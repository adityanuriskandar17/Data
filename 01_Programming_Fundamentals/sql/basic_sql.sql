-- ============================================
-- SQL DASAR UNTUK DATA ENGINEER
-- ============================================
-- Bahasa Indonesia

-- --- DDL (Data Definition Language) ---
CREATE DATABASE data_warehouse;

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date DATE NOT NULL,
    total_amount DECIMAL(10, 2),
    status VARCHAR(20) DEFAULT 'pending'
);

-- ALTER TABLE
ALTER TABLE customers ADD COLUMN phone VARCHAR(20);
ALTER TABLE customers DROP COLUMN phone;
ALTER TABLE customers ALTER COLUMN email SET NOT NULL;

-- --- DML (Data Manipulation Language) ---
INSERT INTO customers (name, email) VALUES ('Budi Santoso', 'budi@email.com');
INSERT INTO customers (name, email) VALUES ('Siti Rahayu', 'siti@email.com');

UPDATE customers SET email = 'budi.baru@email.com' WHERE customer_id = 1;

DELETE FROM customers WHERE customer_id = 2;

-- --- SELECT & FILTERING ---
SELECT * FROM customers;
SELECT name, email FROM customers WHERE customer_id = 1;
SELECT * FROM orders WHERE total_amount > 100000 ORDER BY order_date DESC;
SELECT * FROM orders LIMIT 10 OFFSET 20;

-- --- AGGREGASI ---
SELECT COUNT(*) AS total_order FROM orders;
SELECT status, COUNT(*) AS jumlah, SUM(total_amount) AS total
FROM orders
GROUP BY status
HAVING COUNT(*) > 5;

-- --- JOIN ---
SELECT c.name, o.order_date, o.total_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id;

SELECT c.name, o.order_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id;

SELECT c.name, o.order_date
FROM customers c
RIGHT JOIN orders o ON c.customer_id = o.customer_id;

SELECT c.name, o.order_date
FROM customers c
FULL OUTER JOIN orders o ON c.customer_id = o.customer_id;

-- --- SUBQUERY ---
SELECT * FROM orders
WHERE customer_id IN (
    SELECT customer_id FROM customers WHERE email LIKE '%@email.com'
);

SELECT name, (
    SELECT COUNT(*) FROM orders WHERE orders.customer_id = customers.customer_id
) AS total_order
FROM customers;
