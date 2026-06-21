# ============================================
# APACHE SPARK UNTUK DATA ENGINEERING
# ============================================
# Bahasa Indonesia
# Jalankan: spark-submit spark_basics.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count, when, to_date, year, month
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

# --- MEMBUAT SPARK SESSION ---
spark = SparkSession.builder \
    .appName("DataEngineering - Belajar Spark") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .getOrCreate()

# --- MEMBACA DATA ---
# CSV
df_csv = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("path/to/file.csv")

# JSON
df_json = spark.read.json("path/to/file.json")

# Parquet (format penyimpanan yang paling efisien)
df_parquet = spark.read.parquet("path/to/file.parquet")

# Dari tabel database (JDBC)
df_jdbc = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/database") \
    .option("dbtable", "schema.table") \
    .option("user", "user") \
    .option("password", "password") \
    .load()

# --- TRANSFORMASI DATA ---
# Filter
df_filtered = df_csv.filter(col("amount") > 1000)

# Select columns
df_selected = df_csv.select("customer_id", "amount", "order_date")

# Add new column
df_with_year = df_csv.withColumn("year", year(to_date(col("order_date"), "yyyy-MM-dd")))

# Group by & aggregasi
df_aggregated = df_csv.groupBy("customer_id").agg(
    sum("amount").alias("total_spent"),
    avg("amount").alias("avg_spent"),
    count("*").alias("order_count")
)

# --- WRITE DATA ---
# Menulis sebagai Parquet
df_aggregated.write \
    .mode("overwrite") \
    .partitionBy("year") \
    .parquet("output/aggregated/")

# Menulis ke tabel database
df_aggregated.write \
    .mode("append") \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/warehouse") \
    .option("dbtable", "analytics.customer_summary") \
    .option("user", "user") \
    .option("password", "password") \
    .save()

# --- CACHE & PERSIST ---
df_cached = df_csv.filter(col("status") == "active").cache()

# --- SQL LANGSUNG DI SPARK ---
df_csv.createOrReplaceTempView("orders")
result = spark.sql("""
    SELECT customer_id, SUM(amount) as total
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
    ORDER BY total DESC
""")

# --- PARTITION & REPARTITION ---
print(f"Jumlah partisi saat ini: {df_csv.rdd.getNumPartitions()}")
df_repartitioned = df_csv.repartition(10, "customer_id")
df_coalesced = df_csv.coalesce(4)  # mengurangi jumlah partisi

spark.stop()
