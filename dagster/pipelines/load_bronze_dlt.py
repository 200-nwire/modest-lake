from dagster import op, job
from sqlalchemy import create_engine, text
import pandas as pd
import requests
from io import BytesIO
import gzip

# Configuration for Trino and Iceberg
TRINO_CONNECTION_STRING = "trino://trino-user@trino:8080/iceberg/bronze"
TABLE_NAME = "network_data"

@op
def fetch_csv():
    """
    Fetches and preprocesses the CSV data from the given URL.
    """
    url = "https://s3.amazonaws.com/botsdataset/botsv1/csv-by-sourcetype/botsv1.stream%3Aldap.csv.gz"
    response = requests.get(url)
    with gzip.open(BytesIO(response.content), mode='rt') as gz_file:
        df = pd.read_csv(gz_file)

    # Format timestamps
    df["_time"] = pd.to_datetime(df["_time"], format="mixed", errors="coerce")
    df["_time"].fillna(pd.Timestamp("1970-01-01 00:00:00"), inplace=True)
    return df

@op
def ingest_csv_to_iceberg(data: pd.DataFrame):
    """
    Inserts rows from the DataFrame into Iceberg via Trino one by one.
    """
    engine = create_engine(TRINO_CONNECTION_STRING)
    with engine.connect() as conn:
        # Create the schema if it doesn't exist
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS bronze"))
        print("Schema 'bronze' created successfully.")

        # Create the table if it doesn't exist
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS bronze.{TABLE_NAME} (
            _serial BIGINT,
            _time TIMESTAMP,
            source VARCHAR,
            sourcetype VARCHAR,
            host VARCHAR,
            index VARCHAR,
            splunk_server VARCHAR,
            _raw VARCHAR
        )
        """
        conn.execute(text(create_table_query))
        print(f"Table '{TABLE_NAME}' created successfully.")

        insert_query = f"""
        INSERT INTO bronze.{TABLE_NAME} VALUES (
            :serial,
            TIMESTAMP ':timestamp',
            :source,
            :sourcetype,
            :host,
            :index,
            :splunk_server,
            :raw
        )
        """

        # Insert rows one by one
        for _, row in data.iterrows():
            timestamp = row["_time"].strftime("%Y-%m-%d %H:%M:%S")

            conn.execute(
                text(insert_query),
                {
                    "serial": row["_serial"],
                    "timestamp": timestamp,
                    "source": row["source"],
                    "sourcetype": row["sourcetype"],
                    "host": row["host"],
                    "index": row["index"],
                    "splunk_server": row["splunk_server"],
                    "raw": row["_raw"].replace("'", "''"),
                },
            )

        print(f"Successfully ingested {len(data)} rows into bronze.{TABLE_NAME}.")

@job
def load_csv_to_iceberg():
    """
    Dagster job to orchestrate the CSV ingestion pipeline.
    """
    data = fetch_csv()
    ingest_csv_to_iceberg(data)
