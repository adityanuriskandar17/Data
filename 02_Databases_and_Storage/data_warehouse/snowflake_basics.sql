-- ============================================
-- SNOWFLAKE UNTUK DATA WAREHOUSE
-- ============================================

-- --- WAREHOUSE ---
CREATE WAREHOUSE de_wh
  WITH WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 300
  AUTO_RESUME = TRUE;

-- --- DATABASE & SCHEMA ---
CREATE DATABASE de_database;
CREATE SCHEMA bronze;
CREATE SCHEMA silver;
CREATE SCHEMA gold;

-- --- TABLE DENGAN CLUSTERING ---
CREATE TABLE bronze.orders (
    order_id INT,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2),
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
CLUSTER BY (order_date);

-- --- STAGE (untuk file eksternal) ---
CREATE STAGE de_stage
  URL = 's3://my-bucket/data/'
  CREDENTIALS = (AWS_KEY_ID = 'xxx' AWS_SECRET_KEY = 'yyy');

-- --- COPY INTO (load data) ---
COPY INTO bronze.orders
FROM @de_stage/orders/
FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1)
ON_ERROR = 'CONTINUE';

-- --- TASK (scheduled job) ---
CREATE TASK bronze_to_silver
  WAREHOUSE = de_wh
  SCHEDULE = '1 HOUR'
AS
  INSERT INTO silver.orders_clean
  SELECT * FROM bronze.orders
  WHERE total_amount > 0;

-- --- STREAM (CDC / change tracking) ---
CREATE STREAM bronze.orders_stream ON TABLE bronze.orders;

-- Melihat perubahan
SELECT * FROM bronze.orders_stream;

-- --- TIME TRAVEL (query data di masa lalu) ---
SELECT * FROM bronze.orders AT (TIMESTAMP => '2025-01-01 10:00:00');
SELECT * FROM bronze.orders BEFORE (STATEMENT => '8e5d0ca9-...');
