import datetime
import os

import pandas as pd
from dagster import ConfigurableResource, EnvVar
from dagster_dbt import DbtCliResource
from pydantic import Field
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
import dlt

FILE_PATH = os.path.dirname(__file__)
DBT_PROJECT_DIR = os.path.join(FILE_PATH, "./dbt_project")
DATA_URL = os.getenv("DATA_URL")
ENV = os.getenv("DAGSTER_ENV", "LOCAL")


class CsvReaderResource(ConfigurableResource):

    def download_csv(self, input_file, compression: None) -> pd.DataFrame:
        print("fetching data from ", input_file)
        if compression:
            return pd.read_csv(input_file, compression=compression)
        return pd.read_csv(input_file)


class TrinoIcebergResource(ConfigurableResource):
    host: str = Field(description="Trino host")
    catalog: str = Field(description="Trino catalog")
    username: str = Field(description="Trino username")
    port: int = Field(description="Trino port", default=8080)

    def create_engine(self) -> Engine:
        connection_string = (
            f"trino://{self.username}@{self.host}:{self.port}/{self.catalog}"
        )
        engine = create_engine(connection_string)
        return engine

    def fetch_data(self, schema, table) -> pd.DataFrame:
        """Fetch data from Trino and return as a DataFrame."""
        query = f"SELECT * FROM {schema}.{table}"
        with self.create_engine().connect() as connection:
            result = pd.read_sql(query, connection)
        print("Fetching data from Trino")
        return result

    def write_data(self, schema, table, df: pd.DataFrame):
        """Write DataFrame to Trino using the Iceberg connector."""
        with self.create_engine().connect() as connection:
            df.to_sql(
                table,
                con=connection,
                schema=schema,
                if_exists="append",
                index=False,
                method="multi",
                chunksize=500,
            )
        print("Writing data to Trino")

    def execute(self, query: str):
        with self.create_engine().connect() as connection:
            connection.execute(text(query))
        print("Executing query on Trino")

    def create_schema(self, schema):
        query = f"CREATE SCHEMA IF NOT EXISTS {schema}"
        self.execute(query)
        print("Creating schema in Trino")

    def dlt_ingest(self, schema, table, df: pd.DataFrame):
        pipeline = dlt.pipeline(
            pipeline_name=f"pipeline_{schema}_{table}",
            destination=dlt.destinations.sqlalchemy(self.create_engine()),
            dataset_name=schema,
        )
        pipeline.run(df, dataset_name=schema, table_name=table)
        print("Writing data to Trino using DLT")


resource_def = {
    "LOCAL": {
        "csv_source": CsvReaderResource(),
        "trino": TrinoIcebergResource(
            host=os.getenv("TRINO_HOST"),
            catalog=os.getenv("ICEBERG_CATALOG"),
            username=os.getenv("TRINO_USER"),
            port=int(os.getenv("TRINO_PORT", 8080)),
        ),
        "dbt": DbtCliResource(project_dir=DBT_PROJECT_DIR, target="local"),
    },
    "PROD": {
        "csv_source": CsvReaderResource(),
        "trino": TrinoIcebergResource(
            host=os.getenv("TRINO_HOST"),
            catalog=os.getenv("ICEBERG_CATALOG"),
            username=os.getenv("TRINO_USER"),
            port=int(os.getenv("TRINO_PORT", 8080)),
        ),
        # "dbt": DbtCliResource(project_dir=DBT_PROJECT_DIR, target="prod"),
    },
}
