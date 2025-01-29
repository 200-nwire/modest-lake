-- models/stream_ldap.sql

{{ config(
    materialized='table'
) }}

with SourceData as (
SELECT *
FROM {{ source('raw', 'stream_ldap') }}
),
DeduplicatedData AS (
    SELECT DISTINCT * FROM SourceData
)
,cleaned_data AS (
    SELECT DISTINCT
        CAST(_serial AS BIGINT) AS _serial,
        -- Parse and validate timestamps
        CASE
            WHEN TRY(CAST(_time AS TIMESTAMP)) IS NOT NULL THEN CAST(_time AS TIMESTAMP)
            ELSE NULL
        END AS _time,
        -- Extract fields from _raw JSON
        JSON_EXTRACT_SCALAR(_raw, '$.src_ip') AS src_ip,
        JSON_EXTRACT_SCALAR(_raw, '$.dest_ip') AS dest_ip,
        CAST(JSON_EXTRACT_SCALAR(_raw, '$.src_port') AS INTEGER) AS src_port,
        CAST(JSON_EXTRACT_SCALAR(_raw, '$.dest_port') AS INTEGER) AS dest_port,
        JSON_EXTRACT_SCALAR(_raw, '$.user') AS user,
        -- Map event_type based on raw data
        CASE
            WHEN JSON_EXTRACT_SCALAR(_raw, '$.event') LIKE '%login%' THEN 'login_attempt'
            WHEN JSON_EXTRACT_SCALAR(_raw, '$.event') LIKE '%query%' THEN 'ldap_query'
            ELSE 'unknown'
        END AS event_type,
        CASE 
        WHEN json_extract_scalar(_raw, '$.message_type') IS NOT NULL THEN 
            REPLACE(LOWER(json_extract_scalar(_raw, '$.message_type')), ' ', '_')
        ELSE NULL
    	END AS message_type,
        -- Extract and map status
        CASE
            WHEN JSON_EXTRACT_SCALAR(_raw, '$.status') IN ('success', 'failed') THEN JSON_EXTRACT_SCALAR(_raw, '$.status')
            ELSE 'unknown'
        END AS status
    FROM DeduplicatedData
    WHERE _serial IS NOT NULL
      AND _raw IS NOT NULL
),

sla_and_priorities AS (
    SELECT
        *,
        -- Add SLA thresholds (example: event delay threshold in minutes)
        CASE
            WHEN _time IS NOT NULL AND DATE_DIFF('minute', _time, CURRENT_TIMESTAMP) > 30 THEN 'breach'
            ELSE 'within_sla'
        END AS sla_status,
        -- Assign priority based on event_type
        CASE
            WHEN event_type = 'login_attempt' AND status = 'failed' THEN 'high'
            WHEN event_type = 'ldap_query' THEN 'medium'
            ELSE 'low'
        END AS priority
    FROM cleaned_data
)

SELECT
    _serial,
    _time,
    src_ip,
    dest_ip,
    src_port,
    dest_port,
    user,
    event_type,
    status,
    sla_status,
    priority
FROM sla_and_priorities