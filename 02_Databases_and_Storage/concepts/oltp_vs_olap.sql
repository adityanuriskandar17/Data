-- ============================================
-- OLTP vs OLAP: Perbedaan dan Contoh
-- ============================================

-- --- OLTP (Online Transaction Processing) ---
-- Optimasi untuk: INSERT, UPDATE, DELETE yang cepat
-- Biasanya dinormalisasi (3NF)

CREATE TABLE oltp_orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    qty INT NOT NULL,
    unit_price DECIMAL(10,2),
    order_date TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20)
);
-- Index untuk lookup cepat
CREATE INDEX idx_oltp_customer ON oltp_orders(customer_id);

-- --- OLAP (Online Analytical Processing) ---
-- Optimasi untuk: SELECT, aggregasi, analisis
-- Biasanya denormalisasi (star schema)

CREATE TABLE olap_fact_sales (
    sale_id SERIAL,
    date_key INT,
    customer_key INT,
    product_key INT,
    qty INT,
    unit_price DECIMAL(10,2),
    discount DECIMAL(10,2),
    total_amount DECIMAL(10,2)
);
-- Partition by date untuk scanning yang efisien
-- PARTITION BY RANGE (date_key)

CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id INT,
    name VARCHAR(100),
    email VARCHAR(255),
    city VARCHAR(100),
    segment VARCHAR(50),
    effective_date DATE,
    end_date DATE,
    is_current BOOLEAN
);

CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id INT,
    product_name VARCHAR(200),
    category VARCHAR(50),
    brand VARCHAR(50),
    unit_cost DECIMAL(10,2)
);

-- --- ACID vs BASE ---
-- ACID: Atomicity, Consistency, Isolation, Durability
--   -> PostgreSQL, MySQL (OLTP)
--
-- BASE: Basically Available, Soft state, Eventually consistent
--   -> Cassandra, MongoDB (NoSQL)
