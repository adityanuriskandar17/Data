# Data Engineering — Studi Kasus & Interview Preparation

Berdasarkan diskusi tentang Medallion Architecture, biaya query, dan tata kelola data.

---

## 📖 Ringkasan Studi Kasus

### Latar Belakang
Perusahaan menggunakan **Medallion Architecture** (Bronze → Silver → Gold). Tim Data Analyst sering melakukan query langsung ke **Bronze layer** (raw data) dengan alasan data di Gold tidak up-to-date.

### Masalah
1. **Biaya query besar** — Bronze tidak punya partitioning/clustering, full scan setiap query
2. **CREATE OR REPLACE** — Analyst membuat tabel sendiri dari Bronze, duplikasi data menumpuk
3. **Gold tidak fresh** — Pipeline batch (setiap 6 jam), sementara analyst butuh data real-time
4. **Tidak ada governance** — Siapa pun bisa query/buat tabel di mana pun

---

## 🏗️ Arsitektur yang Direkomendasikan

### Hot Path + Cold Path

```
Source (Kafka/PubSub)
        │
        ├──► HOT PATH (Stream) ──► Hot Gold (update tiap 5-15 menit)
        │       Spark Streaming        Partition per JAM
        │                              Data: hari ini SAJA
        │                              Biaya: rendah (scan 1 hari)
        │
        └──► COLD PATH (Batch) ──► Cold Gold (update tiap 6 jam)
                Airflow + dbt          Partition per HARI
                                       Data: historis lengkap
                                       Biaya: rendah (partition pruning)
```

### Medallion + Governance

```
Bronze ──► Silver ──► Gold
  │          │          │
  │          │          ├── Hot Gold (real-time, partition per jam, expire 3 hari)
  │          │          └── Cold Gold (final, partition per hari, source of truth)
  │          │
  │          ├── Authorized Views (read-only untuk analyst)
  │          └── IAM: VIEWER saja, tidak boleh CREATE/DROP/ALTER
  │
  └── IAM: hanya Data Engineer yang boleh CREATE/DROP/ALTER
```

---

## 🛠️ Solusi Teknis

### 1. Atur IAM & Permission

```sql
-- Analyst: hanya bisa SELECT, tidak bisa CREATE/DROP/ALTER
GRANT roles/bigquery.dataViewer ON DATASET bronze TO "group:analysts"
GRANT roles/bigquery.dataViewer ON DATASET silver TO "group:analysts"
GRANT roles/bigquery.dataViewer ON DATASET gold TO "group:analysts"

-- Dataset khusus untuk eksperimen (auto-expire 3 hari)
CREATE SCHEMA analytics_temp
OPTIONS (default_table_expiration_days = 3)
GRANT roles/bigquery.dataEditor ON DATASET analytics_temp TO "group:analysts"
```

### 2. Buat Hot Gold Layer

```sql
-- Hot Gold: update tiap 15 menit via micro-batch
CREATE TABLE gold.daily_sales_hot (
    order_hour TIMESTAMP,
    customer_id INT64,
    total_amount FLOAT64,
    order_count INT64
)
PARTITION BY DATE(order_hour)
CLUSTER BY customer_id
OPTIONS (partition_expiration_days = 3);
```

### 3. Authorized Views

```sql
-- View read-only yang sudah filter kolom & partisi
CREATE VIEW bronze.orders_safe AS
SELECT order_id, customer_id, amount, status
FROM bronze.orders_raw
WHERE _partitiondate >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY);
```

### 4. Monitoring & Alerting

```sql
-- Deteksi CREATE OR REPLACE oleh analyst
SELECT user_email, query, destination_table,
       total_bytes_billed / (1024*1024*1024) AS gb_billed
FROM `region-us.INFORMATION_SCHEMA.JOBS_BY_PROJECT`
WHERE statement_type IN ('CREATE_TABLE_AS_SELECT', 'CREATE_OR_REPLACE_TABLE')
  AND user_email NOT LIKE '%data-engineering@%'
  AND DATE(creation_time) = CURRENT_DATE();
```

### 5. Self-Service Gold

- Tanya ke analyst: data seperti apa yang mereka butuhkan?
- Bangun gold table yang sesuai kebutuhan (tidak perlu CREATE OR REPLACE)
- Dashboard Looker/Tableau langsung SELECT dari Gold

---

## 💬 Interview Questions & Jawaban

### Pertanyaan 1: "Apa itu Medallion Architecture?"

**Jawaban:**

> Medallion Architecture adalah pendekatan berlapis untuk data lakehouse dengan tiga layer:
>
> - **Bronze**: Data mentah, append-only, format asli dari source. Tidak boleh diubah.
> - **Silver**: Data sudah dibersihkan, tipe data benar, duplikat dihapus, tervalidasi.
> - **Gold**: Data agregat siap pakai untuk bisnis, bentuk star schema, langsung bisa diquery BI tools.
>
> Keuntungannya: traceability (bisa lacak dari Gold ke Bronze), data quality meningkat tiap layer, dan multi-purpose — data scientist pakai Bronze, analyst pakai Gold.

---

### Pertanyaan 2: "Bagaimana cara menekan biaya query di Big Query / Snowflake?"

**Jawaban:**

> Ada beberapa strategi:
>
> 1. **Partitioning**: potong tabel per hari/bulan. Query hanya baca partisi relevan, bukan full scan.
> 2. **Clustering**: urutkan data dalam partisi. Filter kolom cluster jadi lebih cepat.
> 3. **SELECT kolom saja**: jangan SELECT * jika hanya butuh 3 kolom.
> 4. **Materialized View**: simpan hasil aggregasi yang sering dipakai.
> 5. **Hot/Cold separation**: data hari ini di Hot Gold (partition per jam), data lama di Cold Gold (partition per hari).
> 6. **Dry run**: selalu cek estimasi biaya sebelum query besar.
>
> Biasanya kombinasi partitioning + clustering saja sudah bisa turunkan biaya 70-90%.

---

### Pertanyaan 3: "Tim Analyst sering query Bronze langsung karena data Gold basi. Bagaimana solusinya?"

**Jawaban:**

> Ini masalah umum. Solusinya bukan memblokir Bronze, tapi mempercepat Gold.
>
> Saya akan buat **Hot Gold layer** — gold table yang di-update setiap 15 menit via streaming atau micro-batch. Data hot gold hanya berisi data hari ini (partition per jam, auto-expire 3 hari), jadi biayanya kecil.
>
> Untuk data final, tetap pakai **Cold Gold** yang dijalankan setiap 6 jam via Airflow/dbt.
>
> Dengan ini, analyst bisa pakai Hot Gold untuk data real-time (biaya rendah, fresh) dan Cold Gold untuk data historis yang akurat.

---

### Pertanyaan 4: "Analyst sering CREATE OR REPLACE TABLE sendiri dari Bronze. Bagaimana?"

**Jawaban:**

> Ini dua sisi masalah: teknis dan kultural.
>
> **Teknis:**
> - Cabut izin CREATE/DROP/ALTER dari dataset Bronze/Silver/Gold untuk group analyst.
> - Beri dataset khusus `analytics_temp` dengan `default_table_expiration_days = 3` untuk eksperimen.
> - Gunakan Authorized Views yang read-only.
>
> **Kultural:**
> - Tanya kenapa mereka perlu CREATE TABLE — biasanya karena Gold tidak sesuai kebutuhan.
> - Bangun self-service gold yang mencakup kebutuhan mereka.
> - Kasih alternatif seperti BigQuery Studio / Notebook yang tidak perlu CREATE TABLE.
>
> **Monitoring:**
> - Alert otomatis kalau terdeteksi CREATE OR REPLACE oleh non-DE.
> - Cost showback: tag biaya query ke tim masing-masing.

---

### Pertanyaan 5: "Apa itu Data Governance dan bagaimana implementasinya?"

**Jawaban:**

> Data Governance adalah kerangka kerja untuk memastikan data dikelola dengan benar: siapa yang boleh akses data apa, bagaimana kualitasnya, dan siapa yang bertanggung jawab.
>
> Implementasi praktis:
> 1. **IAM / RBAC**: atur permission berdasarkan role (Viewer untuk analyst, Editor untuk DE)
> 2. **Data Catalog**: dokumentasi tabel, kolom, pemilik, dan definisi bisnis
> 3. **Data Lineage**: tracking asal-usul data (Bronze → Silver → Gold)
> 4. **Data Quality**: validasi otomatis dengan Great Expectations / dbt test
> 5. **Cost Governance**: tagging per tim, showback biaya query

---

### Pertanyaan 6: "Apa yang dimaksud dengan Hot Path dan Cold Path?"

**Jawaban:**

> Hot Path dan Cold Path adalah arsitektur untuk menangani data real-time dan batch dalam satu sistem.
>
> - **Hot Path**: stream processing (Kafka → Spark Streaming). Latensi detik-menit. Cocok untuk data yang butuh respons cepat. Biaya lebih mahal per GB tapi volume data kecil (hanya data terbaru).
> - **Cold Path**: batch processing (Airflow → dbt/Spark). Latensi jam. Cocok untuk data historis, laporan akhir. Biaya lebih murah per GB.
>
> Di perusahaan ini, saya akan terapkan: Hot Path untuk data hari ini (update tiap 15 menit, partition per jam), Cold Path untuk data lengkap (update tiap 6 jam via dbt, partition per hari).
>
> Hasilnya analyst tetap dapat data fresh tanpa perlu query Bronze.

---

### Pertanyaan 7: "Bagaimana cara meyakinkan stakeholder untuk investasi di data infrastructure?"

**Jawaban:**

> Saya akan menggunakan data, bukan perasaan:
>
> 1. **Ukur biaya saat ini**: query Bronze berapa TB/hari? Berapa dollar?
> 2. **Proyeksikan penghematan**: dengan Hot Gold + partitioning, biaya bisa turun X%
> 3. **Hitung produktivitas analyst**: berapa jam terbuang untuk cleaning data manual?
> 4. **Buat pilot**: implementasi untuk 1 pipeline dulu, tunjukkan hasilnya dalam 2 minggu.
> 5. **Presentasi dalam bahasa bisnis**: bukan "partition pruning" tapi "hemat $X per bulan + analyst bisa deliver laporan 2x lebih cepat".

---

## 📋 Checklist untuk Wawancara

| Topik | Harus Kuasai |
|-------|-------------|
| Medallion Architecture | Bronze/Silver/Gold, kapan pakai masing-masing |
| Partitioning & Clustering | Cara kerja, efisiensi biaya |
| Hot/Cold Path | Stream vs Batch, trade-off |
| IAM & Governance | RBAC, authorized views, dataset isolation |
| dbt | Transformasi SQL, testing, dokumentasi |
| Airflow | Orchestration, DAG, task dependencies |
| BigQuery / Snowflake | Query optimization, cost control |
| Data Quality | Great Expectations, dbt test |
| Communication | Translate teknis ke bahasa bisnis |

---

## 📚 Materi yang Relevan di Folder Ini

| Path | Isi |
|------|-----|
| `roadmap_data_engineer.md` | Learning roadmap lengkap |
| `05_Data_Pipeline_and_Architecture/penjelasan.md` | Medallion, Lambda, Kappa architecture |
| `05_Data_Pipeline_and_Architecture/data_lakehouse/medallion_architecture.sql` | Implementasi SQL Medallion |
| `04_Cloud_Platforms/gcp/bigquery_detailed.sql` | Partitioning, clustering, optimasi biaya |
| `07_Monitoring_and_Observability/pipeline_monitoring.py` | Monitoring & alerting pipeline |
