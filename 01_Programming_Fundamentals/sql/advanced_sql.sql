-- ============================================
-- SQL LANJUTAN UNTUK DATA ENGINEER
-- ============================================

-- --- WINDOW FUNCTIONS ---
-- ROW_NUMBER: memberi nomor urut per grup
SELECT customer_id, order_date, total_amount,
       ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rn
FROM orders;

-- RANK & DENSE_RANK
SELECT product_id, sales,
       RANK() OVER (ORDER BY sales DESC) AS ranking,
       DENSE_RANK() OVER (ORDER BY sales DESC) AS dense_ranking
FROM product_sales;

-- LAG & LEAD: akses baris sebelumnya/sesudahnya
SELECT order_date, total_amount,
       LAG(total_amount, 1) OVER (ORDER BY order_date) AS previous_day,
       LEAD(total_amount, 1) OVER (ORDER BY order_date) AS next_day
FROM orders;

-- SUM kumulatif (running total)
SELECT order_date, total_amount,
       SUM(total_amount) OVER (ORDER BY order_date) AS running_total
FROM orders;

-- --- CTE (Common Table Expression) ---
WITH monthly_sales AS (
    SELECT DATE_TRUNC('month', order_date) AS bulan,
           SUM(total_amount) AS total_sales
    FROM orders
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT bulan, total_sales,
       LAG(total_sales) OVER (ORDER BY bulan) AS prev_month_sales,
       total_sales - LAG(total_sales) OVER (ORDER BY bulan) AS growth
FROM monthly_sales;

-- CTE rekursif untuk hierarki
WITH RECURSIVE org_hierarchy AS (
    SELECT employee_id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL
    UNION ALL
    SELECT e.employee_id, e.name, e.manager_id, oh.level + 1
    FROM employees e
    JOIN org_hierarchy oh ON e.manager_id = oh.employee_id
)
SELECT * FROM org_hierarchy;

-- --- QUERY OPTIMIZATION TIPS ---
-- 1. Gunakan EXPLAIN ANALYZE
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 100;

-- 2. Buat index untuk kolom yang sering di-filter
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_orders_status ON orders(status);

-- 3. Composite index untuk multiple filter
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date);

-- 4. Partitioning untuk tabel besar
CREATE TABLE orders_partitioned (
    order_id INT,
    customer_id INT,
    order_date DATE,
    total_amount DECIMAL(10,2)
) PARTITION BY RANGE (order_date);

CREATE TABLE orders_2024 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
CREATE TABLE orders_2025 PARTITION OF orders_partitioned
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');
