# ============================================
# APACHE AIRFLOW - DAG SEDERHANA
# ============================================
# Bahasa Indonesia

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta
import pandas as pd
import requests

# --- DEFAULT ARGUMENTS ---
default_args = {
    "owner": "data_engineer",
    "depends_on_past": False,
    "email_on_failure": True,
    "email": ["de@company.com"],
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(hours=2),
}

# --- DEFINISI DAG ---
with DAG(
    dag_id="daily_etl_pipeline",
    default_args=default_args,
    description="ETL pipeline harian - extract API, transform, load ke warehouse",
    schedule_interval="0 2 * * *",  # Setiap jam 2 pagi
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["etl", "daily"],
) as dag:

    # --- TASK 1: EKSTRAKSI ---
    def extract_data(**context):
        """Mengambil data dari API eksternal."""
        url = "https://api.example.com/orders"
        params = {
            "date": context["ds"],  # execution date
            "page_size": 1000
        }
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()

        # Simpan ke file sementara
        file_path = f"/tmp/raw_orders_{context['ds']}.json"
        pd.DataFrame(data).to_json(file_path, orient="records")
        return file_path

    task_extract = PythonOperator(
        task_id="extract_data",
        python_callable=extract_data,
        provide_context=True,
    )

    # --- TASK 2: TRANSFORMASI ---
    def transform_data(**context):
        """Transformasi data: cleaning, validasi, konversi tipe."""
        file_path = context["ti"].xcom_pull(task_ids="extract_data")
        df = pd.read_json(file_path)

        # Data cleaning
        df.dropna(subset=["order_id", "customer_id"], inplace=True)
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df = df[df["amount"] > 0]
        df["order_date"] = pd.to_datetime(df["order_date"])

        # Simpan hasil transformasi
        output_path = f"/tmp/transformed_orders_{context['ds']}.parquet"
        df.to_parquet(output_path, index=False)
        return output_path

    task_transform = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
        provide_context=True,
    )

    # --- TASK 3: LOAD KE DATABASE ---
    task_load = PostgresOperator(
        task_id="load_to_dw",
        postgres_conn_id="data_warehouse",
        sql="""
            COPY staging.orders (order_id, customer_id, amount, order_date)
            FROM '/tmp/transformed_orders_{{ ds }}.parquet'
            WITH (FORMAT PARQUET);
        """,
    )

    # --- TASK 4: CLEANUP ---
    task_cleanup = BashOperator(
        task_id="cleanup_temp_files",
        bash_command="rm -f /tmp/*_{{ ds }}.*",
    )

    # --- DEPENDENCIES ---
    task_extract >> task_transform >> task_load >> task_cleanup
