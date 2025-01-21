SELECT
    sourcetype,
    COUNT(*) AS total_events,
    MAX(_time) AS last_event_time,
    MIN(_time) AS first_event_time
FROM staging.clean_network_data
GROUP BY sourcetype;
