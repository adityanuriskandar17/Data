# Penjelasan: Arsitektur Data (Data Architecture)

## Daftar Arsitektur

1. [Lambda Architecture](#1-lambda-architecture)
2. [Kappa Architecture](#2-kappa-architecture)
3. [Medallion Architecture](#3-medallion-architecture)
4. [Data Mesh](#4-data-mesh)
5. [Data Fabric](#5-data-fabric)
6. [Data Lake vs Warehouse vs Lakehouse](#6-data-lake-vs-warehouse-vs-lakehouse)
7. [Perbandingan Arsitektur](#7-perbandingan-arsitektur)

---

## 1. Lambda Architecture

### Konsep
Lambda membagi pipeline menjadi **dua jalur** terpisah:

```
                    ┌──────────────────────────────┐
                    │        DATA SOURCE           │
                    │   (API, DB, IoT, Logs, dll)  │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────┴───────────────┐
                    │          SPLIT DATA          │
                    └──────────────┬───────────────┘
                                   │
            ┌──────────────────────┴──────────────────────┐
            │                                              │
            ▼                                              ▼
┌───────────────────────┐                    ┌───────────────────────┐
│   BATCH LAYER         │                    │   SPEED LAYER         │
│                       │                    │                       │
│  - Proses data lama   │                    │  - Proses data real-  │
│  - Volume besar       │                    │    time (saat ini)    │
│  - Akurat & lengkap   │                    │  - Latensi rendah      │
│  - Contoh: Spark      │                    │  - Contoh: Kafka      │
│    batch job di malam │                    │    Stream, Flink      │
│    hari               │                    │                       │
└───────────┬───────────┘                    └───────────┬───────────┘
            │                                              │
            │       ┌──────────────────────────┐           │
            └──────▶│    SERVING LAYER         │◄──────────┘
                    │   (Gabungkan hasil       │
                    │    batch + speed)         │
                    └──────────────┬───────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │       DATA CONSUMER          │
                    │  (Dashboard, API, Aplikasi)  │
                    └──────────────────────────────┘
```

### Alur Kerja
1. **Batch Layer**: Data historis diproses dalam batch (misal: setiap jam 2 pagi). Hasilnya akurat tapi lambat.
2. **Speed Layer**: Data baru langsung diproses real-time. Hasilnya cepat tapi mungkin kurang akurat (sementara).
3. **Serving Layer**: Menggabungkan hasil batch (data lengkap) + speed (data real-time) untuk konsumen.

### Contoh Kasus
**E-commerce**: Hitung total penjualan hari ini
- **Batch**: Proses data penjualan kemarin (akurat, semua transaksi termasuk refund)
- **Speed**: Proses data penjualan detik ini (cepat, tapi mungkin ada transaksi yang belum selesai)
- **Serving**: Tampilkan jumlah penjualan = data batch kemarin + data speed hari ini

### Kelebihan
- Data historis akurat (batch)
- Data real-time tetap bisa diakses (speed)
- Cocok untuk sistem yang butuh keduanya

### Kekurangan
- **Kompleksitas tinggi**: harus maintain 2 pipeline berbeda
- **Kode ganda**: logika transformasi ditulis 2x (batch & stream)
- **Sulit konsistensi**: hasil batch dan speed bisa berbeda

---

## 2. Kappa Architecture

### Konsep
Kappa menyederhanakan Lambda dengan **hanya satu jalur**: stream processing.

```
                    ┌──────────────────────────────┐
                    │        DATA SOURCE           │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │     STREAM PROCESSING        │
                    │        (SATU PIPELINE)       │
                    │                              │
                    │  - Semua data dianggap       │
                    │    sebagai stream            │
                    │  - Data historis = replay    │
                    │    stream dari awal          │
                    │  - Contoh: Kafka + Kafka     │
                    │    Streams / Flink           │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │       DATA SINK              │
                    │  (Database, Dashboard, API)  │
                    └──────────────────────────────┘
```

### Alur Kerja
1. **Semua data adalah stream**: Data hari ini, data kemarin, data tahun lalu — semua diperlakukan sebagai aliran data.
2. **Replay**: Kalau perlu proses data lama, tinggal "putar ulang" stream dari offset awal.
3. **Satu kode**: Logika transformasi cukup ditulis SEKALI.

### Contoh Kasus
**Deteksi fraud**: 
- Transaksi masuk sebagai stream → langsung diproses → hasil langsung dikirim ke sistem fraud detection
- Kalau mau evaluasi model dengan data bulan lalu, tinggal replay stream dari bulan lalu

### Kelebihan
- **Sederhana**: satu pipeline, satu kode
- **Mudah maintenance**
- **Konsisten**: tidak ada perbedaan batch vs speed

### Kekurangan
- Stream processing framework wajib kuat (Kafka + Flink/Spark Streaming)
- Data dengan volume sangat besar mungkin lambat di-replay
- Tidak semua use case cocok untuk stream (misal: laporan akhir bulan yang butuh data lengkap)

---

## 3. Medallion Architecture

### Konsep
Medallion (arsitektur medali) adalah pendekatan **berlapis** untuk data lakehouse. Data mengalir melalui 3 layer, semakin ke dalam semakin berkualitas.

```
                    ┌────────────────────────────────────────────┐
                    │              DATA SOURCES                 │
                    │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐         │
                    │  │ API │ │  DB │ │ LOG │ │ IoT │  ...     │
                    │  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘         │
                    └─────┼───────┼───────┼───────┼─────────────┘
                          │       │       │       │
                          ▼       ▼       ▼       ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                     BRONZE LAYER (RAW)                     │
    │                                                             │
    │  "Data mentah, apa adanya"                                 │
    │  • Append-only (tidak pernah diubah)                       │
    │  • Format asli: CSV, JSON, Parquet, Avro                   │
    │  • Schema = apa yang datang dari source                    │
    │  • Seperti gudang barang mentah                            │
    │                                                             │
    │  Contoh: bronze.orders_raw, bronze.logs_raw                │
    └──────────────────────────┬──────────────────────────────────┘
                               │
                               │ Proses: validasi, bersihkan,
                               │         konversi tipe, dedup
                               ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                    SILVER LAYER (CLEAN)                    │
    │                                                             │
    │  "Data bersih dan tervalidasi"                             │
    │  • Tipe data sudah benar (int, date, decimal)              │
    │  • Duplikat dihapus                                        │
    │  • Data invalid ditandai / difilter                        │
    │  • Bisa di-query oleh analyst                              │
    │  • Seperti dapur: makanan sudah dicuci & dipotong          │
    │                                                             │
    │  Contoh: silver.orders, silver.customers                   │
    └──────────────────────────┬──────────────────────────────────┘
                               │
                               │ Proses: agregasi, join,
                               │         business logic
                               ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                     GOLD LAYER (AGREGAT)                   │
    │                                                             │
    │  "Data siap pakai untuk bisnis"                            │
    │  • Bentuk star schema (fact + dimension)                   │
    │  • Agregasi per hari / per kategori                        │
    │  • Langsung bisa dipakai dashboard / laporan               │
    │  • Seperti hidangan siap saji                              │
    │                                                             │
    │  Contoh: gold.daily_sales, gold.customer_summary           │
    └──────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
              ┌────────────────────────────────────┐
              │         DATA CONSUMER              │
              │                                    │
              │  ┌─────────┐ ┌─────────┐           │
              │  │BI Tools │ │  ML     │           │
              │  │(Tableau,│ │(Model   │           │
              │  │ Looker) │ │ Training│           │
              │  └─────────┘ └─────────┘           │
              │  ┌─────────┐ ┌─────────┐           │
              │  │Report   │ │   API   │           │
              │  └─────────┘ └─────────┘           │
              └────────────────────────────────────┘
```

### Detail Setiap Layer

| Layer | Nama | Karakteristik | Siapa yang pakai? |
|-------|------|--------------|-------------------|
| 🥉 **Bronze** | Raw | Append-only, format asli, tidak diubah | Hanya data engineer |
| 🥈 **Silver** | Clean | Tervalidasi, tipe benar, deduplikasi | Data engineer + analyst |
| 🥇 **Gold** | Aggregated | Agregat, star schema, siap pakai | Analyst, BI, bisnis |

### Contoh Transformasi

**Bronze → Silver:**
```sql
-- Bronze: data mentah (semua string)
| order_id | amount | order_date |
| "123"    | "50000"| "2025-01-15" |

-- Silver: data bersih (tipe benar)
| order_id (int) | amount (decimal) | order_date (date) |
| 123            | 50000.00         | 2025-01-15        |
```

**Silver → Gold:**
```sql
-- Silver: per transaksi
| order_id | customer_id | amount   | order_date |
| 1        | 100         | 50000.00 | 2025-01-15 |
| 2        | 100         | 75000.00 | 2025-01-16 |
| 3        | 101         | 30000.00 | 2025-01-16 |

-- Gold: agregat per customer
| customer_id | total_spent | avg_order |
| 100         | 125000.00   | 62500.00  |
| 101         | 30000.00    | 30000.00  |
```

### Kelebihan
- **Sederhana**: mudah dipahami, mudah diimplementasi
- **Multi-purpose**: bronze untuk data scientist (data mentah), gold untuk BI (data siap)
- **Traceable**: bisa lacak dari gold → silver → bronze (data lineage)
- **Incremental**: setiap layer hanya tambah kualitas, tidak ada yang dihapus

---

## 4. Data Mesh

### Konsep
Data Mesh mengubah pendekatan dari **sentral** (satu tim DE pegang semua data) menjadi **terdesentralisasi** (setiap domain bisnis punya data masing-masing).

```
┌───────────────────────────────────────────────────────────────────┐
│                    DATA MESH ARCHITECTURE                        │
│                                                                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐   │
│  │  DOMAIN: SALES  │  │ DOMAIN: MARKETING│  │  DOMAIN: LOGISTICS│  │
│  │                 │  │                  │  │                  │   │
│  │  Data: orders,  │  │  Data: campaign, │  │  Data: shipment, │   │
│  │  customers,     │  │  leads,          │  │  warehouse,      │   │
│  │  transactions   │  │  analytics       │  │  delivery        │   │
│  │                 │  │                  │  │                  │   │
│  │  Tim: Sales DE  │  │  Tim: Mktg DE    │  │  Tim: Logist DE  │   │
│  │  + Analyst      │  │  + Analyst       │  │  + Analyst       │   │
│  │                 │  │                  │  │                  │   │
│  │  Output:        │  │  Output:         │  │  Output:         │   │
│  │  domain dataset │  │  domain dataset  │  │  domain dataset  │   │
│  └────────┬────────┘  └────────┬─────────┘  └────────┬────────┘   │
│           │                    │                      │           │
│           └────────┬───────────┴──────────┬───────────┘           │
│                    │                      │                       │
│                    ▼                      ▼                       │
│  ┌─────────────────────────────────────────────────────────┐      │
│  │              DATA INFRASTRUCTURE PLATFORM               │      │
│  │                                                        │      │
│  │  Storage (S3/GCS)  │  Compute (Spark)  │  Catalog      │      │
│  │  Networking        │  Security         │  Governance   │      │
│  └─────────────────────────────────────────────────────────┘      │
│                                                                   │
│  4 Prinsip Data Mesh:                                             │
│  1. Domain Ownership: setiap domain punya & manage datanya       │
│  2. Data as a Product: data diperlakukan seperti produk          │
│  3. Self-serve Platform: infrastruktur shared yang mudah dipakai │
│  4. Federated Governance: aturan standar yang disepakati bersama │
└───────────────────────────────────────────────────────────────────┘
```

### Perbandingan Data Mesh vs Medallion

| Aspek | Medallion | Data Mesh |
|-------|-----------|-----------|
| Siapa pegang data? | Satu tim DE sentral | Masing-masing domain |
| Skala | Cocok untuk 1-50 tim | Cocok untuk 50+ tim |
| Kompleksitas | Rendah-sedang | Tinggi |
| Kapan pakai | Startup, perusahaan kecil | Perusahaan besar, banyak domain |

---

## 5. Data Fabric

### Konsep
Data Fabric adalah arsitektur yang **menghubungkan** semua sumber data (on-premise, cloud, hybrid) secara otomatis dengan bantuan AI/ML.

```
                    ┌──────────────────────────────────────────┐
                    │            DATA FABRIC                   │
                    │                                          │
                    │  ┌──────────┐ ┌──────────┐ ┌──────────┐ │
                    │  │  On-Prem │ │  Cloud A │ │  Cloud B  │ │
                    │  │  DB, DW  │ │  S3, DW  │ │  BigQuery │ │
                    │  └────┬─────┘ └────┬─────┘ └────┬─────┘ │
                    │       │            │            │        │
                    │       └────────────┼────────────┘        │
                    │                    ▼                     │
                    │  ┌───────────────────────────────────┐   │
                    │  │      VIRTUAL DATA LAYER           │   │
                    │  │  (AI/ML untuk otomatisasi)       │   │
                    │  │  • Data discovery otomatis        │   │
                    │  │  • Data catalog otomatis          │   │
                    │  │  • Data quality monitoring        │   │
                    │  │  • Data lineage tracking          │   │
                    │  └───────────────────────────────────┘   │
                    │                    │                     │
                    │                    ▼                     │
                    │  ┌───────────────────────────────────┐   │
                    │  │         DATA CONSUMER             │   │
                    │  │  (Query di manapun, seolah-olah  │   │
                    │  │   data ada di satu tempat)        │   │
                    │  └───────────────────────────────────┘   │
                    └──────────────────────────────────────────┘
```

### Bedanya dengan yang lain
- **Medallion**: fokus pada kualitas data (bronze → silver → gold)
- **Lambda/Kappa**: fokus pada batch vs stream
- **Data Mesh**: fokus pada organisasi dan kepemilikan
- **Data Fabric**: fokus pada **konektivitas dan otomatisasi** antar sistem yang berbeda

---

## 6. Data Lake vs Warehouse vs Lakehouse

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PERBANDINGAN ARSITEKTUR                         │
├─────────────────┬─────────────────┬─────────────────┬───────────────┤
│                 │   DATA LAKE     │  DATA WAREHOUSE │   LAKEHOUSE   │
├─────────────────┼─────────────────┼─────────────────┼───────────────┤
│ Format Data     │ Semua format    │  Terstruktur    │ Semua +       │
│                 │ (CSV, JSON,     │  (tabel, SQL)   │ terstruktur   │
│                 │  parquet, dll)  │                 │               │
├─────────────────┼─────────────────┼─────────────────┼───────────────┤
│ Schema          │ Schema-on-read  │  Schema-on-write│ Keduanya      │
│                 │ (baru ditentukan│  (wajib tentukan│               │
│                 │  saat dibaca)   │  sebelum input) │               │
├─────────────────┼─────────────────┼─────────────────┼───────────────┤
│ Kualitas Data   │ Rendah (raw)    │  Tinggi (bersih)│ Sedang-tinggi │
├─────────────────┼─────────────────┼─────────────────┼───────────────┤
│ Kecepatan Query │ Lambat          │  Cepat          │ Cepat         │
├─────────────────┼─────────────────┼─────────────────┼───────────────┤
│ Biaya           │ Murah           │  Mahal          │ Sedang        │
├─────────────────┼─────────────────┼─────────────────┼───────────────┤
│ Cocok untuk     │ Data scientist, │  BI, Reporting  │ Keduanya      │
│                 │ ML, data mentah │                 │               │
├─────────────────┼─────────────────┼─────────────────┼───────────────┤
│ Contoh Teknologi│ S3, GCS,        │ Redshift,       │ Databricks    │
│                 │ Hadoop HDFS     │ BigQuery,       │ Delta Lake,   │
│                 │                 │ Snowflake       │ Iceberg       │
├─────────────────┼─────────────────┼─────────────────┼───────────────┤
│ ACID Transaction│ ❌ Tidak        │ ✅ Ya           │ ✅ Ya         │
└─────────────────┴─────────────────┴─────────────────┴───────────────┘

                    ┌─────────────────────┐
                    │      LAKEHOUSE      │
                    │   (Gabungan keduanya)│
                    │                     │
                    │  ┌───────────────┐  │
                    │  │  Data Lake    │  │
                    │  │  (murah,      │  │
                    │  │   fleksibel)  │  │
                    │  └───────┬───────┘  │
                    │          │          │
                    │  ┌───────┴───────┐  │
                    │  │ Data Warehouse│  │
                    │  │ (cepat,       │  │
                    │  │  transaksional)│  │
                    │  └───────────────┘  │
                    └─────────────────────┘
```

### Data Lake
- Simpan SEMUA data mentah (struktur, semi-struktur, tidak terstruktur)
- Schema ditentukan saat MEMBACA, bukan saat MENYIMPAN
- **Murah** tapi query lambat

### Data Warehouse
- Simpan data terstruktur yang sudah dibersihkan
- Schema wajib ditentukan SEBELUM data masuk
- **Mahal** tapi query sangat cepat (columnar storage)

### Lakehouse
- Gabungan kelebihan data lake (murah, fleksibel) + warehouse (cepat, ACID)
- Pakai format seperti Delta Lake / Apache Iceberg
- Bisa query langsung data di S3 dengan performa seperti warehouse

---

## 7. Perbandingan Arsitektur

| Arsitektur | Kapan Pakai? | Kelebihan Utama | Kekurangan Utama |
|------------|-------------|-----------------|------------------|
| **Lambda** | Butuh batch + real-time | Akurat & real-time | Kompleks, kode ganda |
| **Kappa** | Hanya real-time, data replay | Sederhana, satu pipeline | Butuh stream infra kuat |
| **Medallion** | Data lakehouse, multi-purpose | Layer jelas, traceable | Bisa lambat kalau terlalu banyak layer |
| **Data Mesh** | Perusahaan besar, banyak domain | Skalabel secara organisasi | Butuh budaya & maturity |
| **Data Fabric** | Banyak sistem berbeda | Otomatis, connected | Teknologi masih berkembang |

### Rekomendasi Pemilihan

```
Mulai dari sini:
│
├── Perusahaan kecil / startup?
│   └── Medallion Architecture ✅ (sederhana, cukup untuk 1 tim DE)
│
├── Perusahaan menengah (3-10 tim)?
│   ├── Ada kebutuhan real-time?
│   │   ├── Ya → Lambda atau Kappa
│   │   └── Tidak → Medallion tetap cukup
│   └── Semua data bisa di-stream?
│       └── Ya → Kappa (lebih sederhana dari Lambda)
│
└── Perusahaan besar (10+ tim, banyak domain)?
    └── Data Mesh (tapi kombinasikan dengan Medallion per domain)
```
