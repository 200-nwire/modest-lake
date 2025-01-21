# BI Lake Data Lineage Pipeline

Complete end-to-end BI lake pipeline.

The project represents a comprehensive **modern data stack** implementation using **Dagster** as the orchestration layer. It focuses on creating a robust data pipeline with clear lineage and modularity. Each stage of the pipeline—from ingestion to analytics—is represented as a dedicated layer, enabling scalability, flexibility, and easy traceability.

## Project Structure

### Core Directories
1. **`analytics/`**
    - **Purpose**: The final layer for serving analytics-ready data.
    - **Contents**: Includes models, metrics, and pre-aggregations (often used in dashboards and APIs).
    - **Example Tools**: Cube.js, Superset.

2. **`assets/`**
    - **Purpose**: Defines reusable data assets and their dependencies in Dagster.
    - **Contents**: Assets representing raw and transformed data entities with lineage tracking.

3. **`cubes/`**
    - **Purpose**: Defines the **semantic layer** for production-ready OLAP cubes.
    - **Contents**: Cube.js configurations (e.g., dimensions, measures, pre-aggregations).
    - **Example Use**: Serving dashboards and APIs with consistent business metrics.

4. **`ingestion/`**
    - **Purpose**: Handles raw data ingestion from various sources (e.g., APIs, files, databases).
    - **Contents**: DLT pipelines, custom scripts, and connectors for loading data into **Iceberg**.
    - **Example Tools**: DLT, Airbyte.

5. **`jobs/`**
    - **Purpose**: Defines Dagster jobs (orchestrations of assets and tasks).
    - **Contents**: Job configurations, schedules, and sensors for pipeline execution.

6. **`shared/`**
    - **Purpose**: Shared utilities and configurations used across the project.
    - **Contents**: Common libraries, helper functions, and constants.

7. **`staging/`**
    - **Purpose**: Represents the **structured data layer** (Silver Layer).
    - **Contents**: Transformed and cleansed data, typically used for analytics and downstream aggregations.
    - **Example Tools**: dbt models for cleaning and normalizing data.

8. **`storage/`**
    - **Purpose**: Configurations and infrastructure for storage solutions.
    - **Contents**: Definitions for S3, Iceberg, and Nessie integrations.
    - **Example**: Iceberg table formats, partitioning strategies, and storage lifecycle policies.

9. **`tests/`**
    - **Purpose**: Ensures pipeline reliability and data quality.
    - **Contents**: Tests for transformations, data validity, and integration checks.
    - **Example Tools**: dbt tests, Dagster asset materialization tests.

---

## Key Features
- **Modular Design**: Each layer (ingestion, staging, analytics) is isolated for clarity and maintainability.
- **Lineage Tracking**: With Dagster assets and jobs, full lineage of data is visible across layers.
- **Semantic Layer**: Cube.js powers a semantic layer for consistent metrics and aggregations.
- **End-to-End Orchestration**: Dagster orchestrates all processes, ensuring reliability and visibility.
- **Version-Controlled Storage**: Iceberg (via Nessie) provides ACID compliance and schema evolution.
- **Data Validation**: dbt tests and Dagster validations ensure high-quality data.
