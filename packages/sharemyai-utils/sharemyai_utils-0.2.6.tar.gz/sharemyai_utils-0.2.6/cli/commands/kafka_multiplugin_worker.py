import os
import json
import shutil
import ssl
import time
import datetime
import requests
import click
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import tqdm
from retry import retry
from retry.api import retry_call
from dotenv import load_dotenv

load_dotenv()

# Assuming these functions are defined elsewhere in your codebase
from cli.cli import (
    post_register_worker, get_and_download_plugin, create_venv,
    install_torch_requirements, install_requirements, install_sharemyai_utils,
    run_plugin, kill_process_on_port, process_inference_job
)

PLUGIN_BASE_DIR = './plugin_cache'
KAFKA_BROKERS = os.getenv('KAFKA_BROKERS', 'localhost:9092').split(',')
KAFKA_USERNAME = os.getenv('KAFKA_USERNAME', 'admin')
KAFKA_PASSWORD = os.getenv('KAFKA_PASSWORD', 'admin')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'inferencerequests')

@click.command(help="Run kafka worker that will dynamically download and run plugins")
@click.option('--reset', default=False, help='Reset the worker')
def run_kafka_multiplugin_worker(reset):
    plugin_processes = {}
    cached_plugins_file = "cached_plugins.json"

    if reset:
        reset_worker()
        return

    worker = post_register_worker()
    click.echo(f'Worker:\n{json.dumps(worker, indent=4, sort_keys=True)}')

    cached_plugins = load_cached_plugins(cached_plugins_file)
    consumer = initialize_consumer(worker['id'])
    click.echo("Consumer initialized and connected. Starting to process messages.")
    while True:
        try: 
            for message in consumer:
                try:
                    job = json.loads(message.value)
                    process_job(job, worker, cached_plugins, plugin_processes)
                    
                    # Commit the offset after successful processing
                    consumer.commit()
                    print(f"Committed offset for partition {message.partition}, offset {message.offset}")

                    # Update and save cached plugins
                    with open(cached_plugins_file, "w") as f:
                        json.dump(cached_plugins, f)
                
                except Exception as e:
                    print(f"Error processing message: {str(e)}")
                    # You might want to implement some error handling here,
                    # such as sending the failed message to a dead-letter queue
        
        except KafkaError as ke:
            print(f"Kafka error occurred: {str(ke)}")
            # Implement appropriate error handling, maybe wait before retrying
            time.sleep(5)
        
        except Exception as e:
            print(f"Unexpected error occurred: {str(e)}")
            # Implement appropriate error handling
            
        # Wait a bit before attempting to grab more messages
        time.sleep(5)

def reset_worker():
    for item in os.listdir(PLUGIN_BASE_DIR):
        item_path = os.path.join(PLUGIN_BASE_DIR, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)
    if os.path.exists("cached_plugins.json"):
        os.remove("cached_plugins.json")
    kill_process_on_port(3030)
    click.echo(f'Deleted all downloaded plugins')

def load_cached_plugins(cached_plugins_file):
    if os.path.exists(cached_plugins_file):
        with open(cached_plugins_file, "r") as f:
            return json.load(f)
    return {}

@retry(tries=3, delay=5, backoff=2)
def create_kafka_consumer(worker_id):
    ssl_context = ssl.create_default_context()
    
    return KafkaConsumer(
        bootstrap_servers=KAFKA_BROKERS,
        group_id=f'plugin-worker-{worker_id}',
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        security_protocol='SASL_SSL',
        sasl_mechanism='SCRAM-SHA-256',
        sasl_plain_username=KAFKA_USERNAME,
        sasl_plain_password=KAFKA_PASSWORD,
        ssl_context=ssl_context
    )

def initialize_consumer(worker_id):
    consumer = create_kafka_consumer(worker_id)
    consumer.subscribe([KAFKA_TOPIC])
    return consumer

def process_job(job, worker, cached_plugins, plugin_processes):
    print(job)
    plugin_id = job['pluginId']
    inference_request_id = job.get("inferenceRequestId", "unknown_id")
    
    # ping the api and get a result id, lets other workers know we got this one 
    token = os.getenv('SESSION_TOKEN')
    base_url = os.getenv('BASE_URL', 'http://localhost:8080/api')
    if not token:
        print("No session token found. Please login first.")
        return
    
    response = requests.get(f"{base_url}/inference/request/process/kafka?workerId={worker['id']}&requestId={inference_request_id}", headers={"Authorization": f"Bearer {token}"})
    print(response)
    inference_result_id = response.json()["id"]
    print(inference_result_id)

    if not is_current_plugin(plugin_id, cached_plugins):
        setup_plugin(plugin_id, cached_plugins, plugin_processes)
    
    wait_for_healthcheck()

    with tqdm.tqdm(desc=f'Processing job {inference_request_id}', unit='step') as pbar:
        retry_call(
            process_inference_job,
            fargs=[
                job['params'].get('prompt', ''),
                job['params'].get('image', ''),
                job['params'],
                cached_plugins[plugin_id]['plugin']['params'],
                inference_result_id
            ],
            tries=3,
            delay=1,
            backoff=2,
            max_delay=10
        )
        pbar.update(1)

def is_current_plugin(plugin_id, cached_plugins):
    if plugin_id not in cached_plugins:
        return False
    current_plugin_name = cached_plugins[plugin_id]['plugin']['name']
    try:
        response = requests.get("http://localhost:3030/")
        return current_plugin_name.lower() in response.text.lower()
    except Exception:
        return False

def setup_plugin(plugin_id, cached_plugins, plugin_processes):
    kill_process_on_port(3030)
    
    if plugin_id in cached_plugins:
        plugin = cached_plugins[plugin_id]['plugin']
        plugin_path = cached_plugins[plugin_id]['plugin_path']
        venv_path = cached_plugins[plugin_id]['venv_path']
        click.echo(f'Using cached plugin: {plugin_id}')
    else:
        plugin, plugin_path = get_and_download_plugin(plugin_id, PLUGIN_BASE_DIR)
        click.echo(f'Plugin downloaded to {plugin_path}')
        venv_path = create_venv(plugin_path)
        click.echo(f'Venv created at {venv_path}')
        install_torch_requirements(venv_path, plugin['torchRequirements'])
        install_requirements(venv_path, plugin['requirements'])
        click.echo(f'Requirements installed')
        cached_plugins[plugin_id] = {
            'plugin': plugin,
            'plugin_path': plugin_path,
            'venv_path': venv_path
        }
    
    install_sharemyai_utils(venv_path)
    pid = run_plugin(venv_path, plugin_path, plugin['name'])
    plugin_processes[plugin_id] = pid

def wait_for_healthcheck():
    while True:
        print('Waiting for healthcheck...')
        try:
            response = requests.get("http://localhost:3030/healthcheck")
            if response.status_code == 200:
                print('Healthcheck passed, continuing...')
                break
        except Exception:
            pass
        print('Healthcheck failed, retrying in 5 seconds...')
        time.sleep(5)

if __name__ == "__main__":
    run_kafka_multiplugin_worker()