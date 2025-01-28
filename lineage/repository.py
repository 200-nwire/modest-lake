from dagster import repository
from dagster import Definitions
from .assets.ingestion_assets import fetch_csv, ingest_to_iceberg
from .jobs.ingestion_job import ingestion_pipeline
from .assets.dbt_assets import dbt_assets
from .jobs.processing_job import processing_pipeline
from .assets.analytics_assets import process_gold_job
from .jobs.analytics_job import analytics_pipeline
from .assets.cubes_assets import refresh_cubejs


ingestion_definitions = Definitions(
    assets=[fetch_raw_data, load_to_bronze],
    jobs=[ingestion_pipeline],
)

processing_definitions = Definitions(
    assets=dbt_assets,
    jobs=[processing_pipeline],
)

refined_definitions = Definitions(
    assets=[process_gold_job],
    jobs=[analytics_pipeline],
)

semantic_definitions = Definitions(
    assets=[refresh_cubejs],
)

@repository
def lineage_repository():
    return [
        *ingestion_definitions.get_all_definitions(),
        *processing_definitions.get_all_definitions(),
        *refined_definitions.get_all_definitions(),
        *semantic_definitions.get_all_definitions(),
    ]
