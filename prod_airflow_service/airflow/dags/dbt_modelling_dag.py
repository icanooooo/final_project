from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

import yaml

opening_command = "dbt run --select "
middle_command = "--target "
closing_command = " --profiles opt/dbt/profiles"

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

        commands.append(cmd)
        
    sources = commands[0]
    fct_dims = commands[1]
    mart = commands[2]

    return sources, fct_dims, mart

