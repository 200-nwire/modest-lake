FROM python:3.10-slim

RUN mkdir -p /opt/dagster/app
WORKDIR /opt/dagster/app
ENV DAGSTER_HOME /opt/dagster/app

RUN pip install dagster-webserver dagster-postgres dagster-aws

# Copy your code and workspace to /opt/dagster/app
COPY ./ /opt/dagster/app/

ENV DAGSTER_PG_USERNAME=your_user
ENV DAGSTER_PG_PASSWORD=your_password
ENV DAGSTER_PG_HOST=postgres
ENV DAGSTER_PG_DB=your_database

# Copy dagster instance YAML to $DAGSTER_HOME
# COPY dagster.yaml /opt/dagster/dagster_home/

RUN pip install -r /opt/dagster/app/requirements.txt



EXPOSE 3000

ENTRYPOINT ["dagster-webserver", "-h", "0.0.0.0", "-p", "3000"]
