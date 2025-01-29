{{ config(materialized='table') }}

with SourceData as (
SELECT *
FROM {{ source('raw', 'stream_ldap') }}
),
DeduplicatedData AS (
    SELECT DISTINCT * FROM SourceData
),
incident_data AS (
    SELECT
        CAST(JSON_EXTRACT_SCALAR(_raw, '$.incident_id') AS BIGINT) AS incident_id,
        CAST(JSON_EXTRACT_SCALAR(_raw, '$.start_time') AS TIMESTAMP) AS start_time,
        CAST(JSON_EXTRACT_SCALAR(_raw, '$.end_time') AS TIMESTAMP) AS end_time,
        DATE_DIFF('minute', 
            CAST(JSON_EXTRACT_SCALAR(_raw, '$.start_time') AS TIMESTAMP), 
            CAST(JSON_EXTRACT_SCALAR(_raw, '$.end_time') AS TIMESTAMP)
        ) AS duration_minutes,
        JSON_EXTRACT_SCALAR(_raw, '$.priority') AS priority,
        CAST(JSON_EXTRACT_SCALAR(_raw, '$.sla_threshold') AS DOUBLE) AS sla_threshold,
        -- Determine SLA compliance
        CASE 
            WHEN DATE_DIFF('minute', 
                CAST(JSON_EXTRACT_SCALAR(_raw, '$.start_time') AS TIMESTAMP), 
                CAST(JSON_EXTRACT_SCALAR(_raw, '$.end_time') AS TIMESTAMP)
            ) <= CAST(JSON_EXTRACT_SCALAR(_raw, '$.sla_threshold') AS DOUBLE) 
            THEN TRUE ELSE FALSE 
        END AS is_sla_compliant,
        JSON_EXTRACT_SCALAR(_raw, '$.incident_type') AS incident_type,
        CAST(JSON_EXTRACT_SCALAR(_raw, '$.affected_user_count') AS INTEGER) AS affected_user_count
    FROM DeduplicatedData
    WHERE _raw IS NOT NULL
)

SELECT * FROM incident_data