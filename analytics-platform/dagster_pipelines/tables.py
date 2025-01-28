TABLE_DEF = {
    "stream_ldap": """
        CREATE TABLE IF NOT EXISTS raw.stream_ldap (
            _serial BIGINT,
            _time TIMESTAMP,
            source VARCHAR,
            sourcetype VARCHAR,
            host VARCHAR,
            index VARCHAR,
            splunk_server VARCHAR,
            _raw VARCHAR
        ) WITH (format = 'PARQUET')
        """
}



def get_defnition(table_name: str) -> str:
    return TABLE_DEF[table_name]