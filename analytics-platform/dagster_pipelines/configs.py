def ldap_events_config():
    return {
        "ops": {
            "ladap_events_stream": {
                {"config": {"input_file": "DATA_URL", "compression": "gzip"}}
            },
            "ingest_to_iceberg": {
                "inputs": {"raw_data": {"from": "ladap_events_stream"}}
            },
        }
    }
