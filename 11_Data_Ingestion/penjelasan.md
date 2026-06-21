# Penjelasan: Data Ingestion untuk Data Engineer

## Apa itu Data Ingestion?

Data Ingestion adalah proses **memasukkan data** dari berbagai sumber ke dalam sistem penyimpanan (database, data warehouse, data lake).

Bayangkan seperti **"pipa air"** — kamu ambil air dari berbagai sumber (sungai, sumur, PDAM), lalu disalurkan ke tempat penampungan.

---

## 3 Skenario Utama dalam Tutorial Ini

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DATA INGESTION                              │
├──────────────────┬──────────────────┬──────────────────────────────┤
│  CSV → Database  │ Database → DB    │ Database → CSV              │
│                  │                  │                              │
│  orders.csv      │ PostgreSQL A     │ PostgreSQL                   │
│       ↓          │       ↓          │       ↓                      │
│  PostgreSQL      │ PostgreSQL B     │ export.csv                   │
│  (ingestion)     │ (ingestion_dest) │                              │
└──────────────────┴──────────────────┴──────────────────────────────┘
```

---

## 1. CSV → PostgreSQL

### Metode yang Tersedia

| Metode | File | Kecepatan | Cocok Untuk |
|--------|------|-----------|-------------|
| **Pandas chunking** | `csv_to_postgres.py --method pandas` | Sedang | File < 100 MB, perlu transformasi |
| **Batch INSERT** | `csv_to_postgres.py --method batch` | Cepat | File 100 MB - 1 GB, perlu validasi |
| **COPY** | `csv_to_postgres.py --method copy` | **TERCEPAT** | File > 1 GB, produksi |

### COPY — Yang Tercepat

COPY adalah fitur native PostgreSQL yang membaca file CSV langsung:

```
csv_to_postgres.py --method copy
```

**Kecepatan:** bisa mencapai **100.000+ rows/detik**. Dibanding INSERT biasa yang hanya 1.000-5.000 rows/detik.

**Cara kerja COPY:**
1. PostgreSQL membaca file CSV langsung dari disk
2. Data diparsing di server (bukan di Python)
3. Ditulis langsung ke halaman data (skip WAL log untuk performa)

### Auto-select method

Gunakan `--method auto` — otomatis pilih metode berdasarkan ukuran file:

| Ukuran File | Method |
|-------------|--------|
| < 100 MB | Pandas (fleksibel) |
| 100 MB - 1 GB | Batch INSERT (validasi) |
| > 1 GB | COPY (tercepat) |

---

## 2. Database A → Database B

### Skenario
Transfer data antar database. Bisa:
- Server berbeda (produksi → staging)
- Database berbeda dalam 1 server
- Schema berbeda (bronze → silver)

### Metode

| Metode | File | Kapan Dipakai |
|--------|------|---------------|
| **ETL (pandas)** | `db_to_db.py --method etl` | Data < 10 juta baris, perlu transformasi |
| **Streaming** | `db_to_db.py --method stream` | Data BESAR, tidak perlu transformasi |
| **Parallel** | `db_to_db.py --method parallel --threads 4` | Data SANGAT BESAR, butuh kecepatan |
| **Aggregation** | `db_to_db.py --method agg` | Transfer + agregasi (contoh: orders → daily_summary) |

### Streaming — Paling Aman untuk Memory

```python
# Data langsung dialirkan dari source ke target
# Tidak pernah disimpan di memory Python
with src_conn.cursor(name="stream_cursor") as src_cur:
    src_cur.execute("SELECT * FROM orders")
    while True:
        rows = src_cur.fetchmany(5000)
        if not rows:
            break
        execute_values(tgt_cur, "INSERT INTO ... VALUES %s", rows)
```

### Parallel — Paling Cepat untuk Data Besar

Bagi data berdasarkan range ID, transfer simultan dengan 4 thread:
```
Thread 1: order_id 1..125.000
Thread 2: order_id 125.001..250.000
Thread 3: order_id 250.001..375.000
Thread 4: order_id 375.001..500.000
```

---

## 3. Database → CSV (Export)

### Metode

| Metode | File | Kapan Dipakai |
|--------|------|---------------|
| **COPY TO** | `postgres_to_csv.py --method copy` | File di SERVER, butuh akses SSH |
| **Streaming** | `postgres_to_csv.py --method stream` | File di LOKAL, data besar |
| **Chunked** | `postgres_to_csv.py --method chunked` | Pecah file besar jadi banyak file kecil |
| **Parallel** | `postgres_to_csv.py --method parallel --threads 4` | Export TERCEPAT, multi-thread |

### Chunked Export

Untuk data SANGAT BESAR, lebih baik pecah jadi beberapa file:
```
orders_001.csv  (100.000 rows)
orders_002.csv  (100.000 rows)
orders_003.csv  (100.000 rows)
...
```
Setiap file bisa diproses secara independen.

---

## 4. Menangani Database Sangat Besar

### Prinsip "Never Load Everything into Memory"

**SALAH:**
```python
df = pd.read_sql("SELECT * FROM orders")  # ❌ Semua data masuk RAM!
```

**BENAR:**
```python
# Baca dalam chunk (batch kecil)
for chunk in pd.read_sql(query, conn, chunksize=50000):
    process(chunk)
```

Atau lebih baik lagi — **streaming cursor**:
```python
with conn.cursor(name="stream") as cur:
    cur.execute(query)
    while True:
        rows = cur.fetchmany(5000)
```

Streaming cursor tidak pernah menyimpan semua data di memory. Data langsung dikirim dari PostgreSQL ke Python dalam batch kecil.

### Teknik untuk Large Data

| Teknik | File | Penjelasan |
|--------|------|------------|
| **Chunking** | `large_db_handling.py --example chunked` | Baca data dalam potongan kecil |
| **Batch processing** | `large_db_handling.py --example batch` | Proses per batch, commit per batch |
| **Parallel processing** | `large_db_handling.py --example parallel` | Bagi data, proses simultan |
| **Progress tracking** | `large_db_handling.py --example progress` | Lihat progress untuk data besar |

---

## 5. Dataset dalam Tutorial Ini

Jalankan `data/generate_data.py` untuk membuat dataset:

| File | Baris | Ukuran (perkiraan) | Isi |
|------|-------|--------------------|-----|
| `products.csv` | 15 | 1 KB | Data produk statis |
| `customers.csv` | 100.000 | ~8 MB | Data pelanggan |
| `orders.csv` | 500.000 | ~50 MB | Data pesanan (tabel utama) |

Untuk simulasi **large data**, ubah parameter:
```bash
python data/generate_data.py --customers 1000000 --orders 5000000
```

---

## 6. Full Pipeline

```bash
python ingestion_orchestrator.py
```

Akan menjalankan urutan:
1. Generate data sample
2. Setup tabel PostgreSQL
3. CSV → PostgreSQL (COPY)
4. DB A → DB B (transfer + agregasi)
5. PostgreSQL → CSV (export)
6. Large data handling demo

---

## 7. Tips untuk Production

1. **Selalu gunakan COPY** untuk load CSV — 10-100x lebih cepat dari INSERT
2. **Streaming cursor** untuk read large data — hindari OOM
3. **Batch commit** — jangan commit setiap 1 baris, commit per 5.000-10.000 baris
4. **Parallel processing** — manfaatkan multi-core CPU
5. **Progress tracking** — untuk data > 1 jam, user harus tahu progressnya
6. **Error handling** — tangkap error per batch, jangan stop di batch pertama yang error
7. **Idempotent** — pipeline harus bisa dijalankan ulang tanpa duplikasi data
