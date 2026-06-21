-- ============================================
-- MEDALLION ARCHITECTURE (Bronze/Silver/Gold)
-- ============================================
-- Data Lakehouse dengan pendekatan medallion
-- Bahasa Indonesia

-- Konsep:
-- Bronze:  Data mentah, apa adanya dari source (append only)
-- Silver:  Data sudah dibersihkan, validasi, deduplikasi
-- Gold:    Data agregat, siap pakai untuk analisis/BI

-- --- BRONZE LAYER (RAW DATA) ---
-- Data persis seperti dari source, tidak ada perubahan
CREATE SCHEMA bronze;

CREATE TABLE bronze.orders (
    _file_name STRING,
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    -- Raw data (semua string, sesuai source)
    raw_json STRING
);

-- Atau dengan schema inference
CREATE TABLE bronze.orders_raw
USING DELTA
LOCATION '/data/bronze/orders/'
AS SELECT * FROM parquet.`/landing/orders/`;

-- --- SILVER LAYER (CLEAN DATA) ---
-- Data sudah tervalidasi, tipe data benar, duplikat dihapus
CREATE SCHEMA silver;

CREATE TABLE silver.orders (
    order_id STRING NOT NULL,
    customer_id STRING,
    order_date DATE,
    total_amount DECIMAL(12,2),
    status STRING,
    product_id STRING,
    qty INT,
    _loaded_at TIMESTAMP,
    -- Quality check columns
    _is_valid BOOLEAN,
    _validation_error STRING
)
USING DELTA
LOCATION '/data/silver/orders/';

-- Insert dari bronze dengan validasi
INSERT INTO silver.orders
SELECT
    order_id,
    customer_id,
    TO_DATE(order_date, 'yyyy-MM-dd') AS order_date,
    CAST(total_amount AS DECIMAL(12,2)) AS total_amount,
    status,
    product_id,
    CAST(qty AS INT) AS qty,
    CURRENT_TIMESTAMP() AS _loaded_at,
    total_amount IS NOT NULL AND qty > 0 AS _is_valid,
    CASE
        WHEN total_amount IS NULL THEN 'amount null'
        WHEN qty <= 0 THEN 'qty <= 0'
        ELSE NULL
    END AS _validation_error
FROM bronze.orders_raw;

-- --- GOLD LAYER (AGREGAT / BUSINESS) ---
CREATE SCHEMA gold;

CREATE TABLE gold.daily_sales (
    order_date DATE,
    product_category STRING,
    total_orders BIGINT,
    total_qty BIGINT,
    total_revenue DECIMAL(16,2),
    avg_order_value DECIMAL(12,2)
)
USING DELTA
LOCATION '/data/gold/daily_sales/';

INSERT INTO gold.daily_sales
SELECT
    o.order_date,
    p.category AS product_category,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(o.qty) AS total_qty,
    SUM(o.total_amount) AS total_revenue,
    AVG(o.total_amount) AS avg_order_value
FROM silver.orders o
JOIN silver.products p ON o.product_id = p.product_id
WHERE o._is_valid = TRUE
GROUP BY o.order_date, p.category;
