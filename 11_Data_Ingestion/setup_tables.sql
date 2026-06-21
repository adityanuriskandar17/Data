-- ============================================
-- SETUP TABEL TARGET UNTUK DATA INGESTION
-- ============================================
-- Jalankan di PostgreSQL sebelum ingestion

-- Buat schema
CREATE SCHEMA IF NOT EXISTS ingestion;

-- --- TABEL CUSTOMERS ---
CREATE TABLE IF NOT EXISTS ingestion.customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255),
    city VARCHAR(50),
    province VARCHAR(50),
    phone VARCHAR(20),
    created_at DATE,
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- --- TABEL PRODUCTS ---
CREATE TABLE IF NOT EXISTS ingestion.products (
    product_id VARCHAR(10) PRIMARY KEY,
    product_name VARCHAR(200),
    category VARCHAR(50),
    unit_price DECIMAL(12, 2),
    stock INT,
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- --- TABEL ORDERS (tabel utama, besar) ---
CREATE TABLE IF NOT EXISTS ingestion.orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    product_id VARCHAR(10),
    product_name VARCHAR(200),
    category VARCHAR(50),
    qty INT,
    unit_price DECIMAL(12, 2),
    total_amount DECIMAL(14, 2),
    order_date TIMESTAMP,
    status VARCHAR(20),
    city VARCHAR(50),
    province VARCHAR(50),
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index untuk query performance
CREATE INDEX IF NOT EXISTS idx_orders_customer ON ingestion.orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_date ON ingestion.orders(order_date);
CREATE INDEX IF NOT EXISTS idx_orders_status ON ingestion.orders(status);

-- --- TABEL DESTINASI LAIN (untuk db_to_db) ---
CREATE SCHEMA IF NOT EXISTS ingestion_dest;

CREATE TABLE IF NOT EXISTS ingestion_dest.orders_summary (
    order_date DATE,
    category VARCHAR(50),
    total_orders INT,
    total_revenue DECIMAL(16, 2),
    avg_order_value DECIMAL(12, 2),
    _ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
