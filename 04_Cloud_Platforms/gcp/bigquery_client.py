# ============================================
# BIGQUERY CLIENT — PYTHON
# ============================================
# Bahasa Indonesia
#
# Install: pip install google-cloud-bigquery
# Setup: export GOOGLE_APPLICATION_CREDENTIALS="sa-key.json"

from google.cloud import bigquery
import pandas as pd
from typing import Optional, List, Dict

# --- KONEKSI ---
client = bigquery.Client(project="my-project")

# ============================================
# 1. QUERY → DATAFRAME
# ============================================

def query_to_df(sql: str) -> pd.DataFrame:
    """Jalankan SQL, hasil langsung jadi DataFrame pandas."""
    df = client.query(sql).to_dataframe()
    print(f"Query selesai: {len(df)} baris, {len(df.columns)} kolom")
    return df

df = query_to_df("SELECT * FROM `my-project.de_learning.orders` LIMIT 100")

# ============================================
# 2. QUERY → ITERATOR (untuk data besar)
# ============================================

def query_iterate(sql: str):
    """Untuk data besar: hasil tidak dimuat semua ke memory."""
    rows = client.query(sql, job_config=bigquery.QueryJobConfig(
        allow_large_results=True
    ))
    for row in rows:
        yield dict(row)  # yield = kirim satu per satu

for row in query_iterate("SELECT * FROM `my-project.de_learning.orders`"):
    print(row["order_id"], row["amount"])

# ============================================
# 3. LOAD DATA DARI DATAFRAME KE BIGQUERY
# ============================================

def df_to_bigquery(
    df: pd.DataFrame,
    table_id: str,
    write_disposition: str = "WRITE_APPEND"
):
    """Upload DataFrame langsung ke BigQuery."""
    job = client.load_table_from_dataframe(
        df,
        table_id,
        job_config=bigquery.LoadJobConfig(
            write_disposition=write_disposition,
            # WRITE_TRUNCATE = hapus & tulis ulang
            # WRITE_APPEND = tambahkan
            # WRITE_EMPTY = hanya jika kosong
            autodetect=True
        )
    )
    job.result()  # tunggu sampai selesai
    print(f"Loaded {len(df)} baris ke {table_id}")

df_to_bigquery(df, "my-project.de_learning.daily_upload")

# ============================================
# 4. LOAD DATA DARI GCS
# ============================================

def load_from_gcs(
    gcs_uri: str,
    table_id: str,
    format: str = "PARQUET"
):
    """Load file dari GCS (Google Cloud Storage) ke BigQuery."""
    job_config = bigquery.LoadJobConfig(
        source_format=format,
        write_disposition="WRITE_TRUNCATE",
        autodetect=True
    )
    load_job = client.load_table_from_uri(
        gcs_uri, table_id, job_config=job_config
    )
    load_job.result()
    print(f"Loaded dari {gcs_uri} ke {table_id}")

load_from_gcs(
    "gs://my-bucket/data/orders/*.parquet",
    "my-project.de_learning.orders"
)

# ============================================
# 5. EXPORT DATA KE GCS
# ============================================

def export_to_gcs(
    table_id: str,
    gcs_uri: str,
    format: str = "PARQUET"
):
    """Export tabel BigQuery ke GCS."""
    extract_job = client.extract_table(
        table_id,
        gcs_uri,
        job_config=bigquery.ExtractJobConfig(
            destination_format=format
        )
    )
    extract_job.result()
    print(f"Exported {table_id} ke {gcs_uri}")

export_to_gcs(
    "my-project.de_learning.orders",
    "gs://my-bucket/exports/orders-*.parquet"
)

# ============================================
# 6. MANAGE TABEL & DATASET
# ============================================

def create_dataset(dataset_id: str, location: str = "asia-southeast1"):
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = location
    client.create_dataset(dataset, exists_ok=True)
    print(f"Dataset {dataset_id} siap")

def list_tables(dataset_id: str) -> List[str]:
    tables = client.list_tables(dataset_id)
    return [t.table_id for t in tables]

def delete_table(table_id: str):
    client.delete_table(table_id, not_found_ok=True)
    print(f"Table {table_id} dihapus")

# ============================================
# 7. CEK BIAYA SEBELUM QUERY (Dry Run)
# ============================================

def estimate_cost(sql: str) -> int:
    """Cek berapa GB yang akan diproses (GRATIS untuk dry run)."""
    job_config = bigquery.QueryJobConfig(dry_run=True)
    job = client.query(sql, job_config=job_config)
    bytes_processed = job.total_bytes_processed
    gb = bytes_processed / (1024**3)
    print(f"Akan memproses: {gb:.2f} GB")
    print(f"Biaya ~ ${gb * 5:.4f}")  # ~$5/TB
    return bytes_processed

estimate_cost("SELECT * FROM `my-project.de_learning.orders`")

# ============================================
# 8. QUERY DENGAN PARAMETER (anti SQL injection)
# ============================================

def query_with_params(customer_id: int, min_amount: float) -> pd.DataFrame:
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("customer_id", "INT64", customer_id),
            bigquery.ScalarQueryParameter("min_amount", "FLOAT64", min_amount)
        ]
    )
    sql = """
        SELECT * FROM `my-project.de_learning.orders`
        WHERE customer_id = @customer_id
          AND amount > @min_amount
    """
    return client.query(sql, job_config=job_config).to_dataframe()

# ============================================
# 9. SCHEDULED QUERY (via API)
# ============================================

def create_scheduled_query(
    sql: str,
    schedule: str = "every 24 hours",
    dataset_id: str = "de_learning",
    destination_table: str = "daily_summary"
):
    """Buat query berjadwal (seperti cron job)."""
    from google.cloud import bigquery_datatransfer

    transfer_client = bigquery_datatransfer.DataTransferServiceClient()
    parent = transfer_client.common_project_path("my-project")

    config = bigquery_datatransfer.TransferConfig(
        destination_dataset_id=dataset_id,
        display_name="daily-summary-job",
        data_source_id="scheduled_query",
        params={
            "query": sql,
            "destination_table_name_template": destination_table,
            "write_disposition": "WRITE_TRUNCATE"
        },
        schedule=schedule,
    )
    transfer_client.create_transfer_config(parent=parent, transfer_config=config)
    print(f"Scheduled query dibuat: {schedule}")


# ============================================
# 10. FULL EXAMPLE: PIPELINE SEDERHANA
# ============================================

def daily_etl_pipeline():
    """Contoh pipeline harian: GCS → BigQuery → Transform → Export."""
    print("=== Pipeline dimulai ===")

    # Step 1: Load raw dari GCS
    load_from_gcs(
        "gs://my-bucket/raw/orders/*.parquet",
        "my-project.bronze.orders"
    )

    # Step 2: Transform dengan SQL
    sql = """
        CREATE OR REPLACE TABLE `my-project.silver.orders` AS
        SELECT
            order_id,
            customer_id,
            PARSE_DATE('%Y%m%d', CAST(order_date AS STRING)) AS order_date,
            CAST(amount AS FLOAT64) AS amount,
            CURRENT_TIMESTAMP() AS processed_at
        FROM `my-project.bronze.orders`
        WHERE amount IS NOT NULL AND amount > 0
    """
    client.query(sql).result()
    print("Silver table siap")

    # Step 3: Agregasi gold
    sql_gold = """
        CREATE OR REPLACE TABLE `my-project.gold.daily_sales` AS
        SELECT
            order_date,
            COUNT(*) AS total_orders,
            SUM(amount) AS total_revenue,
            AVG(amount) AS avg_order_value
        FROM `my-project.silver.orders`
        GROUP BY order_date
    """
    client.query(sql_gold).result()
    print("Gold table siap")

    print("=== Pipeline selesai ===")
