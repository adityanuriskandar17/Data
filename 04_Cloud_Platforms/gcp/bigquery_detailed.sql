-- ============================================
-- BIGQUERY — LENGKAP UNTUK DATA ENGINEER
-- ============================================
-- Google Cloud Console > BigQuery > Editor
-- Bahasa Indonesia

-- ============================================
-- 1. DASAR-DASAR BIGQUERY
-- ============================================

-- BigQuery adalah data warehouse SERVERLESS.
-- Artinya: tidak perlu urus server, langsung query.
-- Bayar per jumlah data yang diproses (bukan per jam).

-- --- 1.1. SELECT SEDERHANA ---
SELECT * FROM `bigquery-public-data.samples.gsod` LIMIT 10;

-- --- 1.2. HITUNG BIAYA SEBELUM QUERY ---
-- Penting! Di BigQuery, biaya dihitung dari data yang diproses.
-- Selalu cek dulu sebelum query besar:
-- Di console: klik "ESTIMATE" atau pakai:

SELECT COUNT(*) FROM `bigquery-public-data.samples.gsod`;
-- Baris ini memproses ~1.5 GB (gratis untuk public dataset)


-- ============================================
-- 2. DATASET & TABEL
-- ============================================

-- --- 2.1. MEMBUAT DATASET ---
-- Dataset = folder yang berisi tabel-tabel
-- Bisa dibuat via SQL atau Console

CREATE SCHEMA IF NOT EXISTS de_learning
  OPTIONS (
    location = 'asia-southeast1',
    description = 'Dataset untuk belajar data engineering'
  );

-- --- 2.2. MEMBUAT TABEL ---
-- Cara 1: Table dengan schema ditentukan
CREATE TABLE de_learning.customers (
    customer_id INT64 NOT NULL,
    name STRING,
    email STRING,
    city STRING,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Cara 2: Table dari hasil query (CREATE AS SELECT)
CREATE TABLE de_learning.customers_backup AS
SELECT * FROM de_learning.customers;

-- Cara 3: External table (langsung baca file di GCS)
CREATE EXTERNAL TABLE de_learning.orders_external
OPTIONS (
    format = 'PARQUET',
    uris = ['gs://my-bucket/orders/*.parquet']
);

-- --- 2.3. INGERT DATA ---
INSERT INTO de_learning.customers (customer_id, name, email, city)
VALUES
    (1, 'Budi Santoso', 'budi@email.com', 'Jakarta'),
    (2, 'Siti Rahayu', 'siti@email.com', 'Bandung'),
    (3, 'Ali Wibowo', 'ali@email.com', 'Surabaya');

-- Insert dari hasil query
INSERT INTO de_learning.customers
SELECT id, name, email, city FROM de_learning.customers_raw;


-- ============================================
-- 3. TIPE DATA DI BIGQUERY
-- ============================================

-- BigQuery punya tipe data khusus yang tidak ada di SQL biasa:

CREATE TABLE de_learning.data_types_demo (
    -- Tipe standar
    id INT64,                               -- Integer
    name STRING,                            -- String / teks
    price FLOAT64,                          -- Float / desimal
    is_active BOOL,                         -- Boolean
    created DATE,                           -- Tanggal (tanpa waktu)
    order_time TIMESTAMP,                   -- Tanggal + waktu (UTC)
    order_time_local DATETIME,              -- Tanggal + waktu (lokal)
    order_time_ny TIME,                     -- Waktu saja

    -- Tipe khusus BigQuery
    event_ts TIMESTAMP,                     -- Microsecond precision
    metadata JSON,                          -- JSON (native!)
    ip_address STRING,                      -- Untuk IP (simpan sebagai string)

    -- Tipe REPEATED / ARRAY (list dalam satu baris)
    tags ARRAY<STRING>,                     -- Array of strings
    scores ARRAY<INT64>,                    -- Array of integers

    -- Tipe STRUCT / RECORD (nested, seperti JSON object)
    address STRUCT<
        street STRING,
        city STRING,
        zip STRING
    >,

    -- Tipe GEOGRAPHY (untuk data spasial)
    location GEOGRAPHY
);

-- Contoh INSERT dengan JSON
INSERT INTO de_learning.data_types_demo (id, name, metadata, tags, address, location)
VALUES (
    1,
    'Budi',
    PARSE_JSON('{"age": 25, "hobby": ["coding", "reading"]}'),
    ['data', 'engineering'],
    STRUCT('Jl. Merdeka', 'Jakarta', '12345'),
    ST_GEOGPOINT(106.8, -6.2)  -- Longitude, Latitude
);

-- Query JSON
SELECT
    id,
    JSON_EXTRACT_SCALAR(metadata, '$.age') AS age,
    JSON_VALUE(metadata, '$.hobby[0]') AS first_hobby
FROM de_learning.data_types_demo;

-- Query ARRAY (UNNEST = membongkar array jadi baris)
SELECT id, tag
FROM de_learning.data_types_demo,
UNNEST(tags) AS tag;


-- ============================================
-- 4. LOAD DATA DARI GCS
-- ============================================

-- --- 4.1. LOAD CSV ---
LOAD DATA INTO de_learning.orders
FROM FILES (
    format = 'CSV',
    uris = ['gs://my-bucket/orders/*.csv'],
    skip_leading_rows = 1  -- skip header
);

-- --- 4.2. LOAD PARQUET ---
LOAD DATA INTO de_learning.orders
FROM FILES (
    format = 'PARQUET',
    uris = ['gs://my-bucket/orders/*.parquet']
);

-- --- 4.3. LOAD JSON ---
LOAD DATA INTO de_learning.orders
FROM FILES (
    format = 'JSON',
    uris = ['gs://my-bucket/orders/*.json']
);

-- --- 4.4. QUERY LANGSUNG TANPA LOAD (External) ---
SELECT *
FROM EXTERNAL_QUERY(
    'my-project.us.my-connection',
    'SELECT * FROM source_table'
);


-- ============================================
-- 5. PARTITIONING & CLUSTERING ★
-- ============================================
-- INI YANG MEMBUAT BIGQUERY CEPAT & MURAH

-- PARTITION: potong tabel berdasarkan kolom (biasanya tanggal).
--   Query hanya baca partisi yang diperlukan → hemat biaya
-- CLUSTER: urutkan data dalam partisi.
--   Query dengan filter kolom cluster jadi lebih cepat

CREATE TABLE de_learning.sales_partitioned (
    sale_id INT64,
    product_name STRING,
    category STRING,
    amount FLOAT64,
    sale_date DATE,
    customer_id INT64
)
PARTITION BY sale_date                    -- 1 partisi per hari
CLUSTER BY customer_id, category;         -- diurutkan dalam partisi

-- Contoh: query ini hanya baca data tanggal 2025-01-15 saja
-- (bukan seluruh tabel!)
SELECT SUM(amount)
FROM de_learning.sales_partitioned
WHERE sale_date = '2025-01-15';

-- Cek berapa banyak data yang diproses:
-- Di Console: lihat "Bytes processed" atau "Bytes billed"

-- --- TIPE PARTITION ---
-- PARTITION BY DATE(...)    → 1 partisi per hari (paling umum)
-- PARTITION BY TIMESTAMP_TRUNC(...) → per jam/hari/bulan
-- PARTITION BY RANGE_BUCKET(...) → range angka
-- PARTITION BY _PARTITIONDATE → untuk ingestion-time partitioning

-- Ingestion-time partitioning (otomatis berdasarkan waktu load)
CREATE TABLE de_learning.logs_ingest_time
PARTITION BY _PARTITIONDATE
OPTIONS (partition_expiration_days = 30)  -- otomatis hapus data >30 hari
AS SELECT * FROM de_learning.logs;


-- ============================================
-- 6. QUERY LANJUTAN
-- ============================================

-- --- 6.1. WINDOW FUNCTIONS ---
SELECT
    customer_id,
    order_date,
    amount,
    ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rn,
    SUM(amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS running_total,
    LAG(amount, 1) OVER (PARTITION BY customer_id ORDER BY order_date) AS prev_amount,
    LEAD(amount, 1) OVER (PARTITION BY customer_id ORDER BY order_date) AS next_amount,
    AVG(amount) OVER (PARTITION BY customer_id) AS avg_per_customer
FROM de_learning.orders;

-- --- 6.2. ARRAY & UNNEST ---
-- UNNEST = ubah array jadi baris
WITH data AS (
    SELECT 1 AS id, ['a','b','c'] AS letters
    UNION ALL
    SELECT 2 AS id, ['x','y'] AS letters
)
SELECT id, letter
FROM data, UNNEST(letters) AS letter;
-- Hasil:
-- 1  a
-- 1  b
-- 1  c
-- 2  x
-- 2  y

-- --- 6.3. NESTED / REPEATED FIELDS ---
-- BigQuery bisa simpan tabel di dalam tabel (nested)
CREATE TABLE de_learning.orders_with_items (
    order_id INT64,
    customer_id INT64,
    items ARRAY<STRUCT<
        product_name STRING,
        qty INT64,
        price FLOAT64
    >>,
    order_total FLOAT64
);

-- Query nested data
SELECT
    order_id,
    item.product_name,
    item.qty * item.price AS item_total
FROM de_learning.orders_with_items,
UNNEST(items) AS item;

-- --- 6.4. WITH (CTE) UNTUK PIPELINE CLEAN ---
WITH
raw_orders AS (
    SELECT * FROM de_learning.orders WHERE amount IS NOT NULL
),
customer_metrics AS (
    SELECT
        customer_id,
        COUNT(*) AS total_orders,
        SUM(amount) AS total_spent,
        AVG(amount) AS avg_order
    FROM raw_orders
    GROUP BY customer_id
),
ranked_customers AS (
    SELECT *,
        RANK() OVER (ORDER BY total_spent DESC) AS rank
    FROM customer_metrics
)
SELECT * FROM ranked_customers WHERE rank <= 10;


-- ============================================
-- 7. BIGQUERY ML (MACHINE LEARNING)
-- ============================================
-- BigQuery bisa bikin model ML langsung pakai SQL!

-- --- 7.1. BUAT MODEL ---
CREATE MODEL de_learning.customer_churn_model
OPTIONS (
    model_type = 'LOGISTIC_REG',
    input_label_cols = ['churned'],
    dataset = 'de_learning',
    model_registry = 'vertex_ai'
) AS
SELECT
    total_orders,
    total_spent,
    avg_order_value,
    days_since_last_order,
    churned
FROM de_learning.training_data;

-- --- 7.2. PREDIKSI ---
SELECT *
FROM ML.PREDICT(
    MODEL de_learning.customer_churn_model,
    (
        SELECT * FROM de_learning.new_customers
    )
);

--- 7.3. REKOMENDASI ---
CREATE MODEL de_learning.product_recommender
OPTIONS (model_type = 'MATRIX_FACTORIZATION') AS
SELECT
    customer_id,
    product_id,
    rating
FROM de_learning.ratings;


-- ============================================
-- 8. OPTIMASI BIAYA & PERFORMA
-- ============================================

-- --- 8.1. SELECT HANYA KOLOM YANG DIBUTUHKAN ---
-- ❌ BURUK: SELECT * membaca semua kolom
-- ✅ BAIK: SELECT hanya kolom yang diperlukan

-- ❌
SELECT * FROM de_learning.orders;
-- ✅
SELECT customer_id, SUM(amount) FROM de_learning.orders GROUP BY 1;

-- --- 8.2. FILTER SEDINI MUNGKIN ---
-- ❌
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER (...) AS rn
    FROM de_learning.orders
) WHERE rn = 1;
-- ✅ (filter rn di outer, tapi orders tetap diproses penuh)

-- Lebih baik filter PARTISI dulu:
SELECT * FROM de_learning.orders
WHERE sale_date >= '2025-01-01'  -- hanya baca partisi ini
  AND customer_id = 100;          -- cluster filter

-- --- 8.3. GUNAKAN APPROXIMATE ---
-- Untuk jutan data besar, hasil approximate jauh lebih cepat:
SELECT APPROX_COUNT_DISTINCT(customer_id) FROM de_learning.orders;
-- vs COUNT(DISTINCT customer_id) -- lebih akurat tapi lambat

-- --- 8.4. MATERIAIZED VIEW ---
-- Simpan hasil query yang sering dipakai
CREATE MATERIALIZED VIEW de_learning.daily_sales_mv AS
SELECT
    sale_date,
    category,
    COUNT(*) AS total_orders,
    SUM(amount) AS total_revenue
FROM de_learning.sales
GROUP BY sale_date, category;

-- Query MV seperti tabel biasa (otomatis pakai data cache)
SELECT * FROM de_learning.daily_sales_mv
WHERE sale_date >= '2025-01-01';

-- --- 8.5. CACHE HASIL QUERY ---
-- BigQuery otomatis cache hasil query selama 24 jam.
-- Query yang SAMA persis (termasuk spasi) akan GRATIS!
-- Manfaatkan: query dashboard sebaiknya persis sama tiap kali


-- ============================================
-- 9. BIGQUERY + PYTHON
-- ============================================
-- Dari Python (file terpisah: bigquery_client.py)
-- from google.cloud import bigquery
--
-- client = bigquery.Client()
-- query = "SELECT * FROM `project.dataset.table`"
-- df = client.query(query).to_dataframe()


-- ============================================
-- 10. TIPS & TRIK
-- ============================================

-- Tips 1: Cek biaya sebelum query
-- Di console: SELECT akan show "This query will process X bytes"

-- Tips 2: Gunakan label untuk tracking biaya per tim/proyek
CREATE TABLE de_learning.orders
OPTIONS (
    labels = [('team', 'analytics'), ('env', 'production')]
);

-- Tips 3: Batasi biaya dengan custom quota
-- Settings > Quotas > "Query usage per day" = limit

-- Tips 4: Gunakan Wildcard Table untuk data terpartisi
SELECT * FROM `my-project.de_learning.orders_2025*`;
-- Membaca semua tabel yang namanya mulai "orders_2025"

-- Tips 5: Time Travel — lihat data 7 hari ke belakang
SELECT * FROM de_learning.orders
FOR SYSTEM_TIME AS OF TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR);

-- Tips 6: Hapus tabel dengan aman (bisa di-restore dalam 7 hari)
-- DROP TABLE de_learning.orders;
-- Dalam 7 hari: bisa di-restore via console atau SQL
