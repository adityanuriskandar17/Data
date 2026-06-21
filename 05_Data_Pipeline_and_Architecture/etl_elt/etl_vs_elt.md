# ETL vs ELT - Panduan Bahasa Indonesia

## ETL (Extract, Transform, Load)
**Data ditransformasi SEBELUM dimuat ke target.**

```
[Source] --> Extract --> Transform (staging) --> Load --> Data Warehouse
```

### Kelebihan ETL
- Cocok untuk data sensitif (PII bisa dibersihkan dulu)
- Warehouse tidak perlu resource besar untuk transformasi
- Kepatuhan regulasi lebih mudah (data sudah bersih sebelum masuk)

### Kekurangan ETL
- Transformasi di awal membuat pipeline kurang fleksibel
- Butuh staging area terpisah
- Transformasi mahal jika data berubah

### Contoh ETL
```python
# Transformasi dilakukan sebelum load
def etl_pipeline():
    # Extract
    data = extract_from_api()
    
    # Transform (dulu)
    data_clean = [d for d in data if d["amount"] > 0]
    data_clean = add_timestamps(data_clean)
    
    # Load (setelah bersih)
    load_to_warehouse(data_clean)
```

## ELT (Extract, Load, Transform)
**Data dimuat dulu, baru ditransformasi di warehouse.**

```
[Source] --> Extract --> Load (raw) --> Transform --> Data Mart
```

### Kelebihan ELT
- Fleksibel - data mentah selalu tersedia
- Transformasi bisa diulang kapan saja
- Cocok untuk data lake dan cloud warehouse (BigQuery, Snowflake)
- Lebih cepat karena hanya 1x load

### Kekurangan ELT
- Warehouse butuh compute power untuk transformasi
- Data mentah memakan storage lebih besar
- Butuh governance yang baik (bronze/silver/gold)

### Contoh ELT (dengan dbt)
```sql
-- Transformasi dilakukan di warehouse dengan SQL
-- bronze.orders -> silver.orders_clean -> gold.daily_sales

-- dbt model: gold/daily_sales.sql
SELECT
    DATE_TRUNC('day', order_date) AS day,
    COUNT(*) AS total_orders,
    SUM(amount) AS total_revenue
FROM {{ ref('orders_clean') }}
GROUP BY 1
```

## Kapan Pakai ETL vs ELT?

| Faktor | ETL | ELT |
|--------|-----|-----|
| Volume Data | Kecil-Sedang | Besar (TB+) |
| Kecepatan Pipeline | Lebih lambat | Lebih cepat |
| Fleksibilitas | Rendah | Tinggi |
| Storage Cost | Rendah | Tinggi |
| Compute di Warehouse | Rendah | Tinggi |
| Data Sensitivity | Tinggi (PII dll) | Rendah |
| Tim Data Engineer | Matang | Modern |

**Rekomendasi:** Untuk data engineering modern, mulai dengan **ELT** dan gunakan tools seperti **dbt** untuk transformasi. Cadangkan ETL hanya untuk kasus khusus (data sensitif, legacy system).
