# Penjelasan: Cloud Platforms untuk Data Engineering

## 1. Apa itu Cloud Computing?
Bayangkan kamu butuh komputer canggih untuk memproses data besar. Daripada beli komputer fisik (mahal, ribet), kamu bisa "menyewa" komputer dari penyedia cloud (AWS, GCP, Azure).

### Keuntungan
- **Bayar sesuai pemakaian**: kalau tidak dipakai, tidak bayar
- **Skalabel**: bisa tambah kapasitas dalam hitungan menit
- **Terurus**: tidak perlu urus hardware

## 2. AWS Services untuk Data Engineering

| Service | Fungsi | Analogi |
|---------|--------|---------|
| **S3** | Menyimpan file (data lake) | Google Drive untuk file besar |
| **Glue** | ETL serverless (Spark) | Pabrik pengolah data otomatis |
| **Redshift** | Data warehouse | Database kolom untuk analisis |
| **Lambda** | Fungsi kecil tanpa server | Robot yang kerja kalau ada trigger |
| **Kinesis** | Streaming data | Kafka versi AWS |
| **EMR** | Cluster Hadoop/Spark | Sewa komputer untuk Spark |

### S3 (Simple Storage Service)
- Simpan file apapun: CSV, JSON, Parquet, gambar
- Organisasi dengan bucket (folder utama) dan key (path file)
- Sangat murah untuk penyimpanan

### Redshift
- Database kolom (columnar), beda dengan PostgreSQL (row-based)
- Columnar: lebih cepat untuk aggregasi (SUM, AVG, COUNT)
- Pakai "Sort Key" untuk urutan penyimpanan dan "Dist Key" untuk distribusi data

## 3. GCP Services untuk Data Engineering

| Service | Fungsi | Mirip AWS |
|---------|--------|-----------|
| **GCS** | Object storage | S3 |
| **BigQuery** | Data warehouse serverless | Redshift |
| **Dataflow** | Stream/batch processing (Beam) | Kinesis + Glue |
| **Pub/Sub** | Messaging | Kinesis |
| **Dataproc** | Managed Spark/Hadoop | EMR |

---

## 4. BIGQUERY — Penjelasan Lengkap

### 4.1. Apa itu BigQuery?

BigQuery adalah **data warehouse serverless** dari Google Cloud.

**Serverless** artinya: tidak perlu urus server. Tidak perlu install, tidak perlu atur CPU/RAM, tidak perlu scaling. Tinggal tulis SQL, jalan.

**Cara kerja:**
```
[Data di GCS / Streaming] → [BigQuery (compute terpisah)] → [Hasil query]
                                    ↕
                         [Penyimpanan terpisah]
                         (tabel di kolom, bukan baris)
```

### 4.2. Konsep PENTING: Separation of Compute & Storage

Di database biasa (PostgreSQL, MySQL), data dan compute ADA DI SERVER YANG SAMA.

Di BigQuery, keduanya **DIPISAHKAN**:

```
Database biasa:        BigQuery:
┌──────────────┐      ┌──────────────┐ ┌──────────────┐
│  Compute +   │      │   Compute    │ │  Compute     │
│  Storage     │      │  (query #1)  │ │ (query #2)   │
│              │      └──────┬───────┘ └──────┬───────┘
│  CPU + RAM   │             │                │
│  + Disk      │             ▼                ▼
└──────────────┘      ┌──────────────────────────────┐
                      │         STORAGE              │
                      │   (Bigtable / Colossus)      │
                      │   Data disimpan di disk       │
                      │   terpisah dari compute       │
                      └──────────────────────────────┘
```

**Artinya:**
- Banyak query bisa jalan BERSAMAAN tanpa saling rebut resource
- Kalau tidak ada query, compute mati → **TIDAK BAYAR** (hanya bayar storage)
- Bisa scale otomatis sampai ribuan server kalau query besar

### 4.3. Kolom vs Baris (Columnar Storage)

BigQuery menyimpan data per **KOLOM**, bukan per **BARIS**.

```
Data asli:
| order_id | customer | amount | city     |
| 1        | Budi     | 50000  | Jakarta  |
| 2        | Siti     | 75000  | Bandung  |

Disimpan per BARIS (PostgreSQL):
[1, Budi, 50000, Jakarta], [2, Siti, 75000, Bandung]

Disimpan per KOLOM (BigQuery → columnar):
order_id:  [1, 2]
customer:  [Budi, Siti]
amount:    [50000, 75000]
city:      [Jakarta, Bandung]
```

**Kenapa columnar lebih cepat untuk analytics?**

Bayangkan query: `SELECT SUM(amount) FROM orders`

- **Row-based**: baca SEMUA kolom (termasuk customer, city yang tidak dipakai) → baca lebih banyak data → lebih lambat & mahal
- **Columnar**: baca HANYA kolom `amount` → lebih sedikit data → lebih cepat & murah

### 4.4. Partitioning — Memotong Tabel

**Masalah:** Tabel dengan 1 tahun data (365 hari). Query untuk 1 hari harus baca seluruh tabel → **mahal**.

**Solusi:** Potong tabel per hari → query hanya baca 1 partisi.

```
Tanpa PARTITION:
┌────────────────────────────────────────────┐
│        1 TAHUN DATA (365 GB)              │
│   Query: baca SEMUA → bayar 365 GB!       │
└────────────────────────────────────────────┘

Dengan PARTITION per hari:
┌────┐ ┌────┐ ┌────┐     ┌────┐
│Jan1│ │Jan2│ │Jan3│ ... │Dec31│
│1GB │ │1GB │ │1GB │     │1GB │
└────┘ └────┘ └────┘     └────┘
Query: baca 1 partisi → bayar 1 GB SAJA!
```

**Cara membuat partitioned table:**
```sql
CREATE TABLE sales
PARTITION BY DATE(sale_date)   -- 1 partisi per hari
AS SELECT * FROM source;
```

**Tipe partition:**
| Tipe | Contoh | Kegunaan |
|------|--------|----------|
| `DATE(col)` | Per hari | Paling umum |
| `TIMESTAMP_TRUNC(col, MONTH)` | Per bulan | Laporan bulanan |
| `RANGE_BUCKET(col, [...]` | Range angka | Harga, usia |
| `_PARTITIONDATE` | Otomatis (waktu load) | Log, event |

### 4.5. Clustering — Mengurutkan Data

**Masalah:** Dalam satu partisi (misal 1 hari), masih banyak data. Filter `WHERE customer_id = 100` masih harus scan seluruh partisi.

**Solusi:** Cluster = urutkan data dalam partisi berdasarkan kolom tertentu.

```sql
CREATE TABLE sales
PARTITION BY DATE(sale_date)
CLUSTER BY customer_id, category
AS SELECT * FROM source;
```

**Visualisasi:**
```
Partisi 2025-01-15 (sebelum cluster):
[cust: 5] [cust: 1] [cust: 9] [cust: 2] [cust: 1] ...

Partisi 2025-01-15 (setelah cluster by customer_id):
[cust: 1] [cust: 1] [cust: 2] [cust: 5] [cust: 9] ...
```

Query `WHERE customer_id = 1` → langsung tahu posisi data (block pruning).

### 4.6. Tipe Data Khusus BigQuery

| Tipe Data | Contoh | Penjelasan |
|-----------|--------|------------|
| `ARRAY<STRING>` | `['a','b','c']` | List dalam satu baris |
| `STRUCT` | `STRUCT('Jl.A', 'Jakarta')` | Object / record dalam satu baris |
| `JSON` | `'{"key":"value"}'` | JSON native (bisa query langsung) |
| `GEOGRAPHY` | `ST_GEOGPOINT(106.8, -6.2)` | Data koordinat / peta |

**ARRAY + UNNEST:**
```sql
-- UNNEST = membongkar array jadi baris
SELECT id, tag
FROM tabel, UNNEST(tags) AS tag;
-- id=1, tag='data'
-- id=1, tag='engineering'
```

### 4.7. Biaya BigQuery

| Komponen | Biaya | Catatan |
|----------|-------|---------|
| **Storage** | ~$0.02/GB/bulan | Data aktif |
| **Long-term storage** | ~$0.01/GB/bulan | Data tidak diubah >90 hari |
| **Query (on-demand)** | ~$5/TB | Bayar per data diproses |
| **Query (flat-rate)** | ~$10k/bulan | Fixed untuk perusahaan besar |

**Cara hemat biaya:**
1. SELECT kolom yang diperlukan, jangan `SELECT *`
2. Gunakan PARTITION + CLUSTER
3. Filter dengan WHERE (terutama kolom partisi)
4. Gunakan APPROX_COUNT_DISTINCT untuk perkiraan cepat
5. Cache: query yang sama dalam 24 jam GRATIS

### 4.8. Membaca & Mengecek Biaya Sebelum Query

```sql
-- Dry run di Python (GRATIS, tidak proses data)
job_config = bigquery.QueryJobConfig(dry_run=True)
job = client.query(sql, job_config=job_config)
bytes = job.total_bytes_processed  # berapa GB yang akan diproses
```

### 4.9. BigQuery ML — Machine Learning pakai SQL

BigQuery bisa buat model ML langsung dengan SQL:

```sql
CREATE MODEL project.dataset.churn_model
OPTIONS(model_type='LOGISTIC_REG') AS
SELECT features, label FROM training_data;
```

Tanpa pindah ke Python, tanpa export data. Semua di BigQuery.

### 4.10. Arsitektur BigQuery dalam Pipeline

```
                         ┌─────────────────────────┐
                         │     DATA SOURCES        │
                         │                         │
                         │  API  │  DB  │  Files    │
                         └───┬───┴──┬───┴───┬─────┘
                             │      │       │
                     ┌───────┘      │       └───────┐
                     ▼              ▼               ▼
              ┌──────────┐  ┌──────────┐  ┌──────────────┐
              │ Streaming │  │  Load    │  │ External     │
              │ (Pub/Sub) │  │ (GCS)    │  │ Query (feder-│
              │  → BQ     │  │  → BQ    │  │ ated)        │
              └─────┬─────┘  └────┬─────┘  └──────┬───────┘
                    │             │                │
                    └─────────────┼────────────────┘
                                  ▼
                    ┌─────────────────────────┐
                    │     BIGQUERY            │
                    │                         │
                    │  Bronze → Silver → Gold │
                    │  (medallion architecture)│
                    └─────────────┬───────────┘
                                  │
                    ┌─────────────┴───────────┐
                    │                         │
                    ▼                         ▼
            ┌──────────────┐        ┌──────────────┐
            │  BI Tools    │        │  Export ke    │
            │  (Looker,    │        │  GCS / API    │
            │   Tableau)   │        │  / ML         │
            └──────────────┘        └──────────────┘
```

---

## 5. Mana yang Harus Dipelajari?

**Rekomendasi:**
1. **AWS**: paling banyak dipakai di industri Indonesia
2. **GCP**: growing fast, BigQuery sangat populer
3. **Azure**: banyak dipakai perusahaan enterprise

Fokus ke SATU cloud dulu sampai mahir, baru pelajari yang lain.
