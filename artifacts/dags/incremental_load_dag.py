from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import json
import boto3
from confluent_kafka import Producer
import pandas as pd
from io import StringIO

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'aqicn_pipeline',
    default_args=default_args,
    description='A pipeline to fetch AQI data, preprocess, store to S3, and publish to Kafka',
    schedule_interval=timedelta(minutes=1),
)

def fetch_aqi_data():
    url = 'https://api.waqi.info/feed/newyork/?token=your_api_token'
    response = requests.get(url)
    data = response.json()
    return data

def preprocess_data(**context):
    raw_data = context['task_instance'].xcom_pull(task_ids='fetch_aqi_data')
    if raw_data.get('status') == 'ok':
        aqi_data = raw_data.get('data')
        processed_data = {
            'date': datetime.fromtimestamp(aqi_data.get('time').get('v')).strftime('%Y-%m-%d %H:%M:%S'),
            'pm25': aqi_data.get('iaqi').get('pm25', {}).get('v', None),
            'o3': aqi_data.get('iaqi').get('o3', {}).get('v', None),
            'no2': aqi_data.get('iaqi').get('no2', {}).get('v', None),
            'co': aqi_data.get('iaqi').get('co', {}).get('v', None)
        }
        return processed_data
    else:
        raise ValueError("Failed to fetch data from AQICN")

def store_to_s3(**context):
    processed_data = context['task_instance'].xcom_pull(task_ids='preprocess_data')
    s3 = boto3.client('s3')
    df = pd.DataFrame([processed_data])
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket='your_s3_bucket', Key=f"aqi_data/{datetime.now().strftime('%Y%m%d%H%M%S')}.csv", Body=csv_buffer.getvalue().encode('utf-8'))
    print(f"Data stored to S3 at {datetime.now().strftime('%Y%m%d%H%M%S')}.csv")

def publish_to_kafka(**context):
    processed_data = context['task_instance'].xcom_pull(task_ids='preprocess_data')
    producer = Producer({'bootstrap.servers': 'localhost:9092'})
    topic = 'aqi_data'
    producer.produce(topic, json.dumps(processed_data).encode('utf-8'))
    producer.flush()
    print("Data published to Kafka")

fetch_data_task = PythonOperator(
    task_id='fetch_aqi_data',
    python_callable=fetch_aqi_data,
    dag=dag,
)

preprocess_data_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    provide_context=True,
    dag=dag,
)

store_to_s3_task = PythonOperator(
    task_id='store_to_s3',
    python_callable=store_to_s3,
    provide_context=True,
    dag=dag,
)

publish_to_kafka_task = PythonOperator(
    task_id='publish_to_kafka',
    python_callable=publish_to_kafka,
    provide_context=True,
    dag=dag,
)
