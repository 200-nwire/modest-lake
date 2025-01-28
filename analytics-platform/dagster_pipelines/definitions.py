from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_modules,
)

from . import assets, resources
from .assets import read_csv_source, ingest_to_iceberg
from .configs import ldap_events_config

daily_schedule = ScheduleDefinition(
    job=define_asset_job(
        name="stream_ldap_job", selection=[read_csv_source, ingest_to_iceberg]
    ),
    cron_schedule="0 0 * * *",
)

all_assets = load_assets_from_modules([assets])

print("Loading definitions for environment: ", resources.ENV)

defs = Definitions(
    assets=all_assets,
    schedules=[daily_schedule],
    resources=resources.resource_def[resources.ENV.upper()],
)
