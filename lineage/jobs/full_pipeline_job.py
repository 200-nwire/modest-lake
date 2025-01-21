from dagster import define_asset_job, repository

from assets.ingestion_assets import fetch_csv, ingest_to_iceberg
from assets.dbt_assets import staging_assets, analytics_assets
from assets.cubes_assets import deploy_cubejs_models

# Define a job to run the full pipeline
full_pipeline_job = define_asset_job(name="full_pipeline", selection="*")

@repository
def bi_lake_pipeline_repo():
    """
    Repository for the BI lake pipeline.
    """
    return [
        fetch_csv,
        ingest_to_iceberg,
        *staging_assets,
        *analytics_assets,
        deploy_cubejs_models,
        full_pipeline
