# ============================================
# SPARK STREAMING (STRUCTURED STREAMING)
# ============================================
# Stream processing dengan Spark

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, window, sum, avg, count
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType

spark = SparkSession.builder \
    .appName("SparkStreaming - Data Engineer") \
    .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoint") \
    .getOrCreate()

# --- SCHEMA UNTUK STREAM DATA ---
schema = StructType([
    StructField("order_id", IntegerType()),
    StructField("customer_id", IntegerType()),
    StructField("product", StringType()),
    StructField("amount", DoubleType()),
    StructField("timestamp", TimestampType())
])

# --- MEMBACA STREAM DARI KAFKA ---
df_stream = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "orders") \
    .option("startingOffsets", "latest") \
    .load()

# Parse JSON dari value Kafka
df_parsed = df_stream \
    .select(from_json(col("value").cast("string"), schema).alias("data")) \
    .select("data.*")

# --- TRANSFORMASI STREAM ---
# Windowed aggregation (tumbling window 5 menit)
df_windowed = df_parsed \
    .withWatermark("timestamp", "10 minutes") \
    .groupBy(
        window(col("timestamp"), "5 minutes"),
        col("product")
    ) \
    .agg(
        sum("amount").alias("total_sales"),
        avg("amount").alias("avg_sales"),
        count("*").alias("order_count")
    )

# --- MENULIS STREAM ---
# Sink ke console (untuk testing)
query_console = df_windowed \
    .writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()

# Sink ke Parquet
query_parquet = df_windowed \
    .writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "/data/streaming/orders_aggregated") \
    .option("checkpointLocation", "/tmp/checkpoint/parquet") \
    .start()

# Sink ke tabel database via JDBC (foreachBatch)
def write_to_postgres(df, epoch_id):
    df.write \
        .mode("append") \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://localhost:5432/warehouse") \
        .option("dbtable", "streaming.order_summary") \
        .save()

query_jdbc = df_windowed \
    .writeStream \
    .outputMode("update") \
    .foreachBatch(write_to_postgres) \
    .start()

# Menunggu stream berjalan
spark.streams.awaitAnyTermination()
