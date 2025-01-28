import pandas as pd
from dagster import (
    AssetExecutionContext,
    MetadataValue,
    asset,
    OpExecutionContext,
    graph_asset,
    AssetIn,
)
from dagster_dbt import DbtCliResource, dbt_assets, get_asset_key_for_model

from .resources import ENV, CsvReaderResource, TrinoIcebergResource, resource_def
import os
from .tables import get_defnition
dbt_parse_invocation = resource_def[ENV.upper()]["dbt"].cli(["parse"]).wait()
dbt_manifest_path = dbt_parse_invocation.target_path.joinpath("manifest.json")


START_DATE = "2023-04-10"


@dbt_assets(manifest=dbt_manifest_path)
def dbt_project_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


@asset(group_name="raw", key_prefix=["raw"], name="raw_csv")
def read_csv_source(
    context: OpExecutionContext, csv_source: CsvReaderResource
) -> pd.DataFrame:
    input_file = os.getenv("DATA_URL")
    compression = "gzip"
    df = csv_source.download_csv(input_file=input_file, compression=compression)
    context.add_output_metadata(
        {
            "num_records": len(df),
            "preview": MetadataValue.md(df.head().to_markdown()),
        }
    )

    return df


@asset(
    required_resource_keys={"trino"},
    group_name="raw",
    key_prefix=["raw"],
    ins={"raw_data": AssetIn(read_csv_source.key)},
    name="stream_ldap",
)
def ingest_to_iceberg(context: OpExecutionContext, raw_data: pd.DataFrame):
    df = raw_data
    df["_time"] = pd.to_datetime(df["_time"], errors="coerce").fillna(
        pd.Timestamp("1970-01-01")
    )
    df["_serial"] = df["_serial"].astype("int64")
    print("create schema")
    # context.resources.trino.dlt_ingest("raw", "stream_ldap", df)
    context.resources.trino.create_schema("raw")
    print("create table")
    context.resources.trino.execute(get_defnition("stream_ldap"))
    print("Writing data to Trino table")
    context.resources.trino.write_data(
        schema="raw",
        table="stream_ldap",
        df=df,
    )

    # Here we could perform some pandas transformations on data
    context.add_output_metadata(
        {
            "num_records": len(df),
            "preview": MetadataValue.md(df.head().to_markdown(index=False)),
        }
    )
    return df


# @graph_asset(
#     group_name="stream_ldap",
#     key_prefix=["stream_ldap"],
# )
# def stream_ldap_events_graph():
#     raw_data = ladap_events_stream()
#     return ingest_to_iceberg(raw_data)
