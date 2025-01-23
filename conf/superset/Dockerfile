FROM apache/superset:latest
# Switching to root to install the required packages
USER root

#RUN apt-get install -y pkg-config
# Example: installing the MySQL driver to connect to the metadata database
# if you prefer Postgres, you may want to use `psycopg2-binary` instead

COPY dashboards databases /app/superset/import/

RUN pip install trino
RUN pip install elasticsearch-dbapi
# Switching back to using the `superset` user
USER superset