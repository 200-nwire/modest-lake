
from dagster import job, op
import subprocess

@op
def run_dbt_transformations():
    result = subprocess.run(["dbt", "run"], cwd="/usr/app", capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        raise Exception("dbt run failed")

@job
def transform_to_silver():
    run_dbt_transformations()
