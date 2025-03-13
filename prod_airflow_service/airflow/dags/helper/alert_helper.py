import requests
import webhook

webhook_url = webhook

def send_failure_to_discord(context):
    task_instance = context.get('task_instance')
    dag_name = context.get('dag').dag_id
    task_name = task_instance.task_id
    exception = context.get('exception')

    message = {
        "content": f"**DAG Failed**\nDAG: {dag_name}\ntask: {task_name}\nException: {exception}\n\n"
    }

    requests.post(webhook_url, json=message)

    