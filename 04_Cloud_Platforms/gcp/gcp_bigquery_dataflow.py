# ============================================
# GOOGLE CLOUD PLATFORM UNTUK DATA ENGINEERING
# ============================================
# GCS, BigQuery, Dataflow, Pub/Sub
# Bahasa Indonesia

from google.cloud import storage, bigquery, pubsub_v1
import json

# ============================================
# GCS (Google Cloud Storage)
# ============================================
storage_client = storage.Client(project="my-project")

def upload_to_gcs(bucket_name: str, source_file: str, destination_blob: str):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    blob.upload_from_filename(source_file)
    print(f"Uploaded ke gs://{bucket_name}/{destination_blob}")

def list_gcs_files(bucket_name: str, prefix: str):
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)
    return [blob.name for blob in blobs]

# ============================================
# BIGQUERY - DATA WAREHOUSE SERVERLESS
# ============================================
bigquery_client = bigquery.Client(project="my-project")

# Membuat dataset dan tabel
dataset = bigquery.Dataset("my-project.de_learning")
dataset.location = "asia-southeast1"
dataset = bigquery_client.create_dataset(dataset, exists_ok=True)

# Load data dari GCS ke BigQuery
job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.PARQUET,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    autodetect=True,
)

load_job = bigquery_client.load_table_from_uri(
    "gs://my-bucket/data/*.parquet",
    "my-project.de_learning.orders",
    job_config=job_config
)
load_job.result()  # Tunggu sampai selesai

# Query BigQuery
query = """
    SELECT customer_id, SUM(amount) as total_spent
    FROM `my-project.de_learning.orders`
    WHERE order_date >= '2025-01-01'
    GROUP BY customer_id
    ORDER BY total_spent DESC
    LIMIT 100
"""
query_job = bigquery_client.query(query)
results = query_job.result()

# Partitioning & Clustering
create_partitioned_table = """
    CREATE TABLE de_learning.orders_partitioned
    PARTITION BY DATE(order_date)
    CLUSTER BY customer_id
    AS SELECT * FROM de_learning.orders;
"""

# ============================================
# PUB/SUB - MESSAGING
# ============================================
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path("my-project", "orders-topic")

def publish_message(data: dict):
    message_data = json.dumps(data).encode("utf-8")
    future = publisher.publish(topic_path, message_data)
    print(f"Published message ID: {future.result()}")

# ============================================
# DATAFLOW (APACHE BEAM)
# ============================================
# Pipeline Dataflow biasanya ditulis dalam file terpisah
# Contoh pipeline sederhana:

"""
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

options = PipelineOptions([
    "--runner=DataflowRunner",
    "--project=my-project",
    "--region=asia-southeast1",
    "--temp_location=gs://temp/dataflow/",
    "--staging_location=gs://temp/dataflow/staging/"
])

with beam.Pipeline(options=options) as p:
    (p
     | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(topic="projects/my-project/topics/orders-topic")
     | "Parse JSON" >> beam.Map(lambda x: json.loads(x.decode("utf-8")))
     | "Filter" >> beam.Filter(lambda x: x["amount"] > 0)
     | "Write to BigQuery" >> beam.io.WriteToBigQuery(
         table="my-project:de_learning.streaming_orders",
         schema="order_id:INTEGER, customer_id:INTEGER, amount:FLOAT",
         write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
     ))
"""
