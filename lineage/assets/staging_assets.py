from dagster import resource, op, AssetIn, asset
from dagster_dbt import dbt_cli_resource, dbt_run_op, dbt_test_op

@resource(config_schema={"project_dir": str, "profiles_dir": str})
def dbt_resource(context):
    """
    Configures the DBT resource for Dagster.
    """
    return dbt_cli_resource.configured({
        "project_dir": context.resource_config["project_dir"],
        "profiles_dir": context.resource_config["profiles_dir"],
    })

@asset(required_resource_keys={"dbt"})
def run_dbt_staging(context):
    """
    Runs DBT models for the staging layer.
    """
    context.resources.dbt.run(models=["tag:staging"])
    context.log.info("DBT staging models executed successfully.")

@asset(required_resource_keys={"dbt"})
def run_dbt_analytics(context):
    """
    Runs DBT models for the analytics layer.
    """
    context.resources.dbt.run(models=["tag:analytics"])
    context.log.info("DBT analytics models executed successfully.")

@asset(required_resource_keys={"dbt"})
def test_dbt_models(context):
    """
    Runs DBT tests for all layers.
    """
    context.resources.dbt.test()
    context.log.info("DBT tests executed successfully.")
