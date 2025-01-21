from dagster import asset
from dagster_dbt import dbt_assets

@dbt_assets(manifest_path="staging/target/manifest.json")
def dbt_staging_assets():
    """
    DBT staging models as Dagster assets.
    These include the transformations applied in the staging layer.
    """
    pass

@dbt_assets(manifest_path="analytics/target/manifest.json")
def dbt_analytics_assets():
    """
    DBT analytics models as Dagster assets.
    These include aggregations and business logic.
    """
    pass
