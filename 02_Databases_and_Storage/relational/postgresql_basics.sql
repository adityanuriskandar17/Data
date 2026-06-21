-- ============================================
-- POSTGRESQL UNTUK DATA ENGINEERING
-- ============================================
-- Bahasa Indonesia

-- Membuat database
CREATE DATABASE de_learning;

-- --- CREATE TABLE dengan berbagai tipe data ---
CREATE TABLE products (
    product_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_name VARCHAR(200) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(12, 2),
    stock INT DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB
);

-- --- INDEXING ---
-- B-tree index (default)
CREATE INDEX idx_products_category ON products(category);

-- Composite index
CREATE INDEX idx_products_category_price ON products(category, price);

-- Partial index
CREATE INDEX idx_products_active ON products(product_id) WHERE is_active = true;

-- Unique index
CREATE UNIQUE INDEX idx_products_name ON products(product_name);

-- --- CONSTRAINTS ---
ALTER TABLE products ADD CONSTRAINT check_price_positive CHECK (price > 0);
ALTER TABLE products ALTER COLUMN stock SET DEFAULT 0;

-- --- VIEW ---
CREATE VIEW active_products AS
SELECT product_id, product_name, category, price
FROM products
WHERE is_active = true;

-- Materialized View (untuk query yang berat)
CREATE MATERIALIZED VIEW monthly_sales_summary AS
SELECT
    DATE_TRUNC('month', order_date) AS month,
    category,
    COUNT(*) AS total_orders,
    SUM(amount) AS total_sales
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY 1, 2
WITH DATA;

-- Refresh materialized view
REFRESH MATERIALIZED VIEW monthly_sales_summary;

-- --- STORED PROCEDURE ---
CREATE OR REPLACE FUNCTION get_customer_orders(p_customer_id INT)
RETURNS TABLE(order_id INT, order_date DATE, total_amount DECIMAL)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT o.order_id, o.order_date, o.total_amount
    FROM orders o
    WHERE o.customer_id = p_customer_id
    ORDER BY o.order_date DESC;
END;
$$;

-- --- TRIGGER ---
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_products_updated_at
    BEFORE UPDATE ON products
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();
