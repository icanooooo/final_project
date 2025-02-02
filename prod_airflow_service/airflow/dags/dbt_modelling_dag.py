from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

dbt_source = "dbt run --profiles /opt/dbt/profiles"