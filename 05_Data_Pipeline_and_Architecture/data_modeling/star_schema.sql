-- ============================================
-- STAR SCHEMA - DATA MODELING
-- ============================================
-- Bahasa Indonesia
-- Contoh: Sales Data Warehouse

-- --- DIMENSION TABLES ---
-- Tabel dimensi: deskriptif, denormalized, SCD (Slowly Changing Dimension)

CREATE TABLE dim_customer (
    customer_sk INT PRIMARY KEY,  -- Surrogate Key
    customer_id INT,              -- Natural Key dari source
    customer_name VARCHAR(100),
    email VARCHAR(255),
    city VARCHAR(100),
    province VARCHAR(100),
    segment VARCHAR(50),          -- Retail, Corporate, SME
    created_date DATE,
    -- SCD Type 2 fields
    valid_from DATE,
    valid_to DATE,
    is_current BOOLEAN DEFAULT true
);

CREATE TABLE dim_product (
    product_sk INT PRIMARY KEY,
    product_id INT,
    product_name VARCHAR(200),
    category VARCHAR(100),
    sub_category VARCHAR(100),
    brand VARCHAR(100),
    unit_cost DECIMAL(12,2),
    unit_price DECIMAL(12,2)
);

CREATE TABLE dim_date (
    date_sk INT PRIMARY KEY,      -- Format: YYYYMMDD
    full_date DATE,
    day INT,
    month INT,
    month_name VARCHAR(20),
    quarter INT,
    year INT,
    day_of_week INT,
    is_weekend BOOLEAN,
    is_holiday BOOLEAN
);

CREATE TABLE dim_store (
    store_sk INT PRIMARY KEY,
    store_id INT,
    store_name VARCHAR(100),
    city VARCHAR(100),
    province VARCHAR(100),
    region VARCHAR(50),
    store_type VARCHAR(50)
);

-- --- FACT TABLE ---
-- Tabel fakta: measure, numeric, foreign key ke dimensi

CREATE TABLE fact_sales (
    sale_id BIGINT IDENTITY(1,1),
    date_sk INT NOT NULL,
    customer_sk INT NOT NULL,
    product_sk INT NOT NULL,
    store_sk INT NOT NULL,
    -- Measures
    quantity INT,
    unit_price DECIMAL(12,2),
    discount DECIMAL(12,2),
    total_amount DECIMAL(12,2),
    cost_amount DECIMAL(12,2),
    profit_amount DECIMAL(12,2),
    -- Foreign Keys
    FOREIGN KEY (date_sk) REFERENCES dim_date(date_sk),
    FOREIGN KEY (customer_sk) REFERENCES dim_customer(customer_sk),
    FOREIGN KEY (product_sk) REFERENCES dim_product(product_sk),
    FOREIGN KEY (store_sk) REFERENCES dim_store(store_sk),
    -- Index untuk performa
    PRIMARY KEY (sale_id, date_sk)
) PARTITION BY RANGE (date_sk);

-- --- QUERY CONTOH ---
-- Total penjualan per kategori per bulan
SELECT
    d.year,
    d.month,
    p.category,
    SUM(f.total_amount) AS total_sales,
    COUNT(*) AS transaction_count
FROM fact_sales f
JOIN dim_date d ON f.date_sk = d.date_sk
JOIN dim_product p ON f.product_sk = p.product_sk
JOIN dim_customer c ON f.customer_sk = c.customer_sk
WHERE d.year = 2025 AND c.segment = 'Corporate'
GROUP BY d.year, d.month, p.category
ORDER BY d.year, d.month, total_sales DESC;
