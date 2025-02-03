from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from helper.alert_helper import send_failure_to_discord

import yaml


opening_command = "dbt run --select "
middle_command = "--target "
closing_command = " --profiles-dir profiles"

def load_config():
    with open("/opt/airflow/dags/configs/app_db.yaml", "r") as file:
        return yaml.safe_load(file)
    
def get_commands(config):
    commands = []

    for name, values in config['models'].items():
        models = ""

        for table in config['models'][name]['tables']:
            models += table['name'] + " "

        cmd = opening_command + models + middle_command + config['models'][name]['target'] + closing_command

        cmd = "docker exec dbt-dbt-1 " + cmd + " --project-dir library_dbt"

        commands.append(cmd)
        
    sources = commands[0]
    fct_dims = commands[1]
    mart = commands[2]

    return sources, fct_dims, mart

def create_dag():
    config=load_config()
    source_cmd, fct_dims_cmd, mart_cmd = get_commands(config)

    default_args = {
        'owner' : 'ican',
        'retries' : 1,
        'retry_delay' : timedelta(seconds=15),
        'on_failure_callback' : send_failure_to_discord,
    }

    with DAG(
        "dbt_modelling_dag",
        start_date=datetime(2025, 2, 2),
        tags=['nigquery_dags', 'dbt_dags'],
        default_args=default_args,
        schedule_interval='@daily',
        catchup=False) as dag:

        source_dag = BashOperator(
            task_id='dbt_run_src',
            bash_command=source_cmd
        )

        fact_and_dim_dag = BashOperator(
            task_id='dbt_run_fact_and_dims',
            bash_command=fct_dims_cmd
        )

        mart_cmd = BashOperator(
            task_id='dbt_run_mart',
            bash_command=mart_cmd
        )

        source_dag >> fact_and_dim_dag >> mart_cmd
    
    return dag

globals()['library_dbt_modelling'] = create_dag()
