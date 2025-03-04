from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests

# Fonksiyon: Resmi indir ve kaydet
def download_image():
    url = "http://host.docker.internal:8090/arrow.png"
    save_path = "/opt/airflow/data/arrow.png"
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
    else:
        raise Exception(f"Failed to download image, status code: {response.status_code}")

# DAG tanımı
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 3, 3),
    "retries": 1,
    "retry_delay": timedelta(seconds=10),
}

dag = DAG(
    "1_download_arrow_image",
    default_args=default_args,
    description="Periodically download an image every minute",
    schedule_interval=timedelta(minutes=1),
    catchup=False,
)

download_task = PythonOperator(
    task_id="download_image",
    python_callable=download_image,
    dag=dag,
)
