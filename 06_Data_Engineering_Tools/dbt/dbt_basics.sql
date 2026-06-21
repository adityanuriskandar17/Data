-- ============================================
-- dbt (DATA BUILD TOOL) - TRANSFORMASI SQL
-- ============================================
-- Bahasa Indonesia
-- File-file ini diletakkan di folder models/ dalam project dbt

-- ============================================
-- Model: bronze -> silver (staging)
-- ============================================
-- File: models/staging/stg_orders.sql

WITH source AS (
    SELECT * FROM {{ source('raw', 'orders') }}
),

renamed AS (
    SELECT
        id AS order_id,
        customer_id,
        order_date::DATE AS order_date,
        amount::DECIMAL(12,2) AS amount,
        status,
        created_at
    FROM source
    WHERE amount IS NOT NULL
)

SELECT * FROM renamed


-- ============================================
-- Model: silver -> gold (mart)
-- ============================================
-- File: models/marts/daily_customer_sales.sql

WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

daily_sales AS (
    SELECT
        o.order_date,
        c.customer_id,
        c.customer_name,
        c.city,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(o.amount) AS total_revenue,
        AVG(o.amount) AS avg_order_value
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.status = 'completed'
    GROUP BY o.order_date, c.customer_id, c.customer_name, c.city
)

SELECT * FROM daily_sales


-- ============================================
-- dbt Test: validasi data
-- ============================================
-- File: tests/assert_positive_amount.sql

SELECT order_id, amount
FROM {{ ref('stg_orders') }}
WHERE amount <= 0


-- ============================================
-- dbt Documentation (schema.yml)
-- ============================================
-- File: models/schema.yml
-- YAML untuk dokumentasi dan test otomatis

/*
version: 2

models:
  - name: stg_orders
    description: "Orders dari source yang sudah dibersihkan"
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: amount
        tests:
          - not_null
          - positive_values:
              > 0

sources:
  - name: raw
    database: dw
    schema: bronze
    tables:
      - name: orders
        freshness:
          warn_after: {count: 6, period: hour}
          error_after: {count: 24, period: hour}
*/
