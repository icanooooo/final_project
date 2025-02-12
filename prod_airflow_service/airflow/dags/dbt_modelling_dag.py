from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from helper.alert_helper import send_failure_to_discord
from airflow.utils.task_group import TaskGroup

import yaml


opening_command = "dbt run --select "
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

        cmd = opening_command + models + closing_command

        cmd = "docker exec dbt-dbt-1 " + cmd + " --project-dir library_dbt"

        commands.append(cmd)
        
    sources, dims, facts, mart = commands[:4]



    return sources, dims, facts, mart

def create_dag():
    config=load_config()
    source_cmd, dims_cmd, facts_cmd, mart_cmd = get_commands(config)

    default_args = {
        'owner' : 'ican',
        'retries' : 1,
        'retry_delay' : timedelta(seconds=15),
        'on_failure_callback' : send_failure_to_discord,
    }

    with DAG(
        "dbt_modelling_dag",
        start_date=datetime(2025, 2, 2),
        tags=['bigquery_dags', 'dbt_dags'],
        default_args=default_args,
        schedule_interval='15 * * * *', # setiap jam dalam menit ke 15 (01.15, 02.15, seterusnya..)
        catchup=False) as dag:

        with TaskGroup("models", dag=dag) as models:
            source_task = BashOperator(
                task_id='dbt_run_src',
                bash_command=source_cmd
            )
            
            dims_task = BashOperator(
                task_id='dbt_run_dim',
                bash_command=dims_cmd
            )

            facts_task = BashOperator(
                task_id='dbt_run_fact',
                bash_command=facts_cmd
            )

            mart_cmd = BashOperator(
                task_id='dbt_run_mart',
                bash_command=mart_cmd
            )
            
            source_task >> [dims_task, facts_task] >> mart_cmd

        snapshot_task = BashOperator(
            task_id='dbt_snapshots',
            bash_command='docker exec dbt-dbt-1 dbt snapshot --project-dir library_dbt'
        )

        models >> snapshot_task
    
    return dag

globals()['library_dbt_modelling'] = create_dag()
