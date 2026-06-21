# ============================================
# AWS UNTUK DATA ENGINEERING
# ============================================
# S3, Glue, Lambda, Redshift
# Bahasa Indonesia

import boto3
import json

# --- KONFIGURASI ---
s3 = boto3.client("s3", region_name="ap-southeast-1")
glue = boto3.client("glue", region_name="ap-southeast-1")
lambda_client = boto3.client("lambda", region_name="ap-southeast-1")

# ============================================
# S3 - PENYIMPANAN DATA
# ============================================

def upload_to_s3(file_path: str, bucket: str, key: str):
    """Upload file ke S3 dengan struktur folder yang rapi."""
    s3.upload_file(
        Filename=file_path,
        Bucket=bucket,
        Key=key,
        ExtraArgs={"StorageClass": "STANDARD_IA"}
    )
    print(f"Uploaded {file_path} ke s3://{bucket}/{key}")

def list_s3_files(bucket: str, prefix: str):
    """List semua file di S3 prefix."""
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    return [obj["Key"] for obj in response.get("Contents", [])]

def s3_to_redshift_copy(bucket: str, key: str, table: str, iam_role: str):
    """Copy data dari S3 ke Redshift."""
    sql = f"""
        COPY {table}
        FROM 's3://{bucket}/{key}'
        IAM_ROLE '{iam_role}'
        FORMAT AS PARQUET;
    """
    return sql

# ============================================
# AWS GLUE - ETL SERVERLESS
# ============================================

# Glue Job (biasanya dijalankan dari console/airflow)
glue_job_config = {
    "Name": "etl-orders-daily",
    "Role": "arn:aws:iam::123456:role/GlueServiceRole",
    "Command": {
        "Name": "glueetl",
        "ScriptLocation": "s3://scripts/etl_orders.py",
        "PythonVersion": "3"
    },
    "DefaultArguments": {
        "--job-language": "python",
        "--TempDir": "s3://temp/glue/",
        "--enable-metrics": "true",
        "--enable-spark-ui": "true",
        "--job-bookmark-option": "job-bookmark-enable"
    },
    "MaxRetries": 2,
    "Timeout": 60,
    "GlueVersion": "4.0",
    "NumberOfWorkers": 5,
    "WorkerType": "G.1X"
}

# ============================================
# AWS LAMBDA - SERVERLESS FUNCTION
# ============================================

def lambda_handler(event, context):
    """Triggered saat file baru diupload ke S3."""
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    print(f"File baru terdeteksi: s3://{bucket}/{key}")

    # Mulai Glue job
    glue.start_job_run(
        JobName="etl-orders-daily",
        Arguments={
            "--input_path": f"s3://{bucket}/{key}",
            "--output_path": "s3://processed/orders/"
        }
    )

    return {"statusCode": 200, "body": json.dumps("OK")}

# ============================================
# REDSHIFT - DATA WAREHOUSE
# ============================================

redshift_config = {
    "host": "my-cluster.xxxx.redshift.amazonaws.com",
    "port": 5439,
    "dbname": "dw",
    "user": "de_user",
    "password": "****"
}

# Sort key dan diststyle untuk performa query
create_table_sql = """
    CREATE TABLE sales_fact (
        sale_id INT IDENTITY(1,1),
        date_key INT NOT NULL,
        product_key INT NOT NULL,
        customer_key INT NOT NULL,
        qty INT,
        amount DECIMAL(12,2)
    )
    DISTKEY(customer_key)
    SORTKEY(date_key);
"""
