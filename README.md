
# Data Pipeline Demo

## Overview
This project demonstrates a complete data pipeline architecture, including:
- **Data Lake**: Iceberg on MinIO with Nessie for cataloging.
- **Query Engines**: Trino, Dremio, and Spark for analytics.
- **Visualization**: Superset, Cube.js, and Vue.js frontend.
- **Machine Learning**: Jupyter Notebook with Spark for ML.

## Services
- **MinIO**: S3-compatible storage backend for Iceberg.
- **Nessie**: Metadata and cataloging for Iceberg.
- **Trino**: Distributed SQL query engine.
- **Dremio**: User-friendly query interface for data lake exploration.
- **Spark**: Batch processing and ML workloads.
- **Superset**: Dashboards and analytics.
- **Cube.js**: API layer for production-ready metrics.
- **Node.js/Koa**: Backend API for frontend interaction.
- **Vue.js**: Frontend for data visualization.

## Setup
1. Install Docker and Docker Compose.
2. Start all services:
   ```bash
   docker-compose up -d
   ```
3. Access tools:
   - MinIO: [http://localhost:9000](http://localhost:9000)
   - Superset: [http://localhost:8088](http://localhost:8088)
   - Dagster: [http://localhost:3000](http://localhost:3000)
   - Jupyter Notebook: [http://localhost:8888](http://localhost:8888)
   - Homer Dashboard: [http://localhost:8081](http://localhost:8081)


https://github.com/splunk/botsv1
