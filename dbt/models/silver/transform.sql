
SELECT
    CAST(src_ip AS STRING) AS source_ip,
    CAST(dest_ip AS STRING) AS destination_ip,
    CAST(bytes AS BIGINT) AS total_bytes,
    CAST(timestamp AS TIMESTAMP) AS event_time
FROM iceberg.bronze.network_data
