from dagster import asset, define_asset_job
from sqlalchemy import create_engine, text
import pandas as pd
import requests
from io import BytesIO
import gzip
import os

@asset
def fetch_csv():
    """
    Fetches and preprocesses the CSV data from a remote source.
    """
    url = os.getenv("DATA_URL")
    response = requests.get(url)
    with gzip.open(BytesIO(response.content), mode="rt") as gz_file:
        df = pd.read_csv(gz_file)

    # Enforce schema and cast types
    df["_time"] = pd.to_datetime(df["_time"], errors="coerce").fillna(pd.Timestamp("1970-01-01"))
    df["_serial"] = df["_serial"].astype("int64")
    return df

@asset
def ingest_to_iceberg(fetch_csv: pd.DataFrame):
    """
    Inserts data from a DataFrame into Iceberg via Trino.
    """
    trino_conn_str = os.getenv("TRINO_CONNECTION_STRING")
    engine = create_engine(trino_conn_str)

    with engine.connect() as conn:
        # Ensure schema exists
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS bronze"))

        # Define table structure
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS bronze.network_data (
            _serial BIGINT,
            _time TIMESTAMP,
            source VARCHAR,
            sourcetype VARCHAR,
            host VARCHAR,
            index VARCHAR,
            splunk_server VARCHAR,
            _raw VARCHAR
        ) WITH (format = 'PARQUET')
        """))

        # Insert data
        for _, row in fetch_csv.iterrows():
            conn.execute(
                text("""
                INSERT INTO bronze.network_data VALUES (
                    :serial, :timestamp, :source, :sourcetype, :host, :index, :splunk_server, :raw
                )
                """),
                {
                    "serial": row["_serial"],
                    "timestamp": row["_time"].strftime("%Y-%m-%d %H:%M:%S"),
                    "source": row["source"],
                    "sourcetype": row["sourcetype"],
                    "host": row["host"],
                    "index": row["index"],
                    "splunk_server": row["splunk_server"],
                    "raw": row["_raw"],
                },
            )

# Define the job
ingestion_job = define_asset_job(name="ingestion_job", selection=["fetch_csv", "ingest_to_iceberg"])
