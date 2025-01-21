WITH raw_data AS (
    SELECT * FROM {{ source('bronze', 'network_data') }}
)
SELECT
    _serial,
    _time,
    source,
    sourcetype,
    host,
    index,
    splunk_server,
    _raw
FROM raw_data
WHERE _time IS NOT NULL;
