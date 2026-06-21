# ============================================
# PROYEK 2: STREAMING PIPELINE
# ============================================
# Kafka -> Spark Streaming -> Sink ke Database
# Bahasa Indonesia

"""
Arsitektur:
1. Producer: Mengirim data pesanan ke Kafka
2. Spark Streaming: Membaca dari Kafka, transformasi, aggregasi
3. Sink: Menulis hasil ke PostgreSQL / file
"""

import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

# =====================
# KAFKA PRODUCER
# =====================

def create_producer():
    return KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: str(k).encode("utf-8")
    )

def generate_order() -> dict:
    """Generate data order random."""
    products = [
        {"id": "P001", "name": "Laptop", "price": 15000000},
        {"id": "P002", "name": "Mouse", "price": 250000},
        {"id": "P003", "name": "Keyboard", "price": 750000},
        {"id": "P004", "name": "Monitor", "price": 3500000},
        {"id": "P005", "name": "Headset", "price": 500000},
    ]
    product = random.choice(products)
    qty = random.randint(1, 5)

    return {
        "order_id": int(time.time() * 1000 * 1000) + random.randint(0, 9999),
        "customer_id": random.randint(1000, 9999),
        "product_id": product["id"],
        "product_name": product["name"],
        "qty": qty,
        "unit_price": product["price"],
        "total_amount": product["price"] * qty,
        "timestamp": datetime.now().isoformat(),
        "status": random.choice(["pending", "confirmed", "shipped"])
    }

def run_producer():
    """Jalankan producer yang mengirim data setiap detik."""
    producer = create_producer()
    topic = "orders"

    print("Producer dimulai... Tekan Ctrl+C untuk berhenti.")

    try:
        while True:
            order = generate_order()
            future = producer.send(
                topic,
                key=order["order_id"],
                value=order
            )
            result = future.get(timeout=10)
            print(f"Sent order {order['order_id']} -> partition {result.partition}")

            time.sleep(random.uniform(0.5, 2.0))  # Random interval

    except KeyboardInterrupt:
        print("\nProducer dihentikan.")
    finally:
        producer.flush()
        producer.close()


# =====================
# SPARK STREAMING (terpisah)
# =====================
# File: spark_streaming_job.py
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, sum, count, avg
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType

spark = SparkSession.builder \
    .appName("StreamingPipeline") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoint") \
    .getOrCreate()

schema = StructType([
    StructField("order_id", IntegerType()),
    StructField("customer_id", IntegerType()),
    StructField("product_id", StringType()),
    StructField("product_name", StringType()),
    StructField("qty", IntegerType()),
    StructField("unit_price", DoubleType()),
    StructField("total_amount", DoubleType()),
    StructField("timestamp", TimestampType()),
    StructField("status", StringType())
])

df_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "orders") \
    .option("startingOffsets", "latest") \
    .load()

df_parsed = df_stream \
    .select(from_json(col("value").cast("string"), schema).alias("data")) \
    .select("data.*")

# Aggregasi per window 1 menit
df_aggregated = df_parsed \
    .withWatermark("timestamp", "5 minutes") \
    .groupBy(window(col("timestamp"), "1 minute"), col("product_id")) \
    .agg(
        sum("total_amount").alias("total_revenue"),
        sum("qty").alias("total_qty"),
        count("*").alias("order_count")
    )

# Sink ke console
query = df_aggregated.writeStream \
    .outputMode("update") \
    .format("console") \
    .option("truncate", "false") \
    .start()

query.awaitTermination()
"""

if __name__ == "__main__":
    run_producer()
