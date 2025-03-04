from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
import os

DATA_DIR = "/opt/airflow/data"
GPKG_URL = "http://host.docker.internal:8090/kontur_population_TR_20231101.gpkg.gz"
GPKG_FILE = "kontur_population_TR_20231101.gpkg"
GZ_FILE = f"{GPKG_FILE}.gz"
DB_CONNECTION = "host=postgres user=airflow password=airflow dbname=airflow"

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 3, 4),
    "retries": 1,
}

dag = DAG(
    "2_import_gpkg",
    default_args=default_args,
    schedule_interval=None,
    catchup=False
)

download_gpkg = BashOperator(
    task_id="download_gpkg",
    bash_command=f"curl -o {DATA_DIR}/{GZ_FILE} {GPKG_URL}",
    dag=dag,
)

extract_gpkg = BashOperator(
    task_id="extract_gpkg",
    bash_command=f"gunzip -c {DATA_DIR}/{GZ_FILE} > {DATA_DIR}/{GPKG_FILE}",
    dag=dag,
)

import_gpkg = BashOperator(
    task_id="import_gpkg",
    bash_command=(
        f"ogr2ogr -f PostgreSQL PG:\"{DB_CONNECTION}\" {DATA_DIR}/{GPKG_FILE} "
        "-progress --config PG_USE_COPY YES"
    ),
    dag=dag,
)

download_gpkg >> extract_gpkg >> import_gpkg