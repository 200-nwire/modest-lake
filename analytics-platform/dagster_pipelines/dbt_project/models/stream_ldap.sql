-- models/stream_ldap.sql

{{ config(
    materialized='table'
) }}

with SourceData as (
SELECT *
FROM {{ source('raw', 'stream_ldap') }}
limit 10
),
DeduplicatedData AS (
    SELECT DISTINCT * FROM SourceData
)
SELECT 
    _serial AS serial,
    CAST(_time AS TIMESTAMP) AS event_timestamp,
    CAST(json_extract_scalar(_raw, '$.src_ip') AS VARCHAR) AS src_ip,
    CAST(json_extract_scalar(_raw, '$.dest_ip') AS VARCHAR) AS dest_ip,
    CAST(json_extract_scalar(_raw, '$.src_port') AS INTEGER) AS src_port,
    CAST(json_extract_scalar(_raw, '$.dest_port') AS INTEGER) AS dest_port,
    CAST(json_extract_scalar(_raw, '$.user') AS VARCHAR) AS user,
    CASE 
        WHEN json_extract_scalar(_raw, '$.message_type') IS NOT NULL THEN 
            REPLACE(LOWER(json_extract_scalar(_raw, '$.message_type')), ' ', '_')
        ELSE NULL
    END AS event_type,
    CAST(json_extract_scalar(_raw, '$.status') AS VARCHAR) AS status

FROM DeduplicatedData