<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:667eea,100:764ba2&height=200&section=header&text=Data%20Engineering%20Learning%20Hub&fontSize=40&fontColor=fff&animation=fadeIn" />
</p>

<p align="center">
  <b>Belajar Data Engineering secara Terstruktur — dari Pemula hingga Siap Kerja 🚀</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Apache_Spark-FDEE21?style=for-the-badge&logo=apachespark&logoColor=black" />
  <img src="https://img.shields.io/badge/Apache_Kafka-231F20?style=for-the-badge&logo=apachekafka&logoColor=white" />
  <img src="https://img.shields.io/badge/Apache_Airflow-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white" />
  <img src="https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white" />
  <img src="https://img.shields.io/badge/AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white" />
  <img src="https://img.shields.io/badge/GCP-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white" />
</p>

---

## 📋 Daftar Isi

- [Apa Ini?](#apa-ini)
- [Struktur Repository](#struktur-repository)
- [Learning Path (11 Modul)](#-learning-path-11-modul)
- [SQL Masterclass + Bonus](#sql-masterclass--bonus)
- [Web App Interaktif](#web-app-interaktif)
- [Cara Mulai Belajar](#cara-mulai-belajar)
- [Testing & Verifikasi](#testing--verifikasi)
- [Lisensi](#lisensi)

---

## 🎯 Apa Ini?

Repository ini adalah **panduan belajar Data Engineering lengkap** dalam Bahasa Indonesia yang mencakup:

| 💡 Konsep & Teori | 🛠️ Praktik Langsung | 🚀 Proyek Nyata |
|-------------------|---------------------|-----------------|
| Penjelasan mendalam di setiap modul | Code Python, SQL, Bash siap jalan | ELT Pipeline, Streaming Pipeline |
| Arsitektur (Medallion, Lambda, Kappa) | Studi kasus dunia nyata | Infrastructure as Code (Terraform) |
| Best practices & design patterns | CI/CD dengan GitHub Actions | Monitoring & Alerting |

---

## 📁 Struktur Repository

```
📦 latihan_de/
├── 📂 01_Programming_Fundamentals/       # Python, SQL, Shell Scripting
├── 📂 02_Databases_and_Storage/          # PostgreSQL, MongoDB, Snowflake, OLTP vs OLAP
├── 📂 03_Big_Data_Technologies/          # Spark, Kafka, Airflow
├── 📂 04_Cloud_Platforms/                # AWS (S3, Glue, Redshift), GCP (BigQuery)
├── 📂 05_Data_Pipeline_and_Architecture/ # Medallion, Star Schema, ETL vs ELT
├── 📂 06_Data_Engineering_Tools/         # dbt, Docker, Terraform, CI/CD
├── 📂 07_Monitoring_and_Observability/   # Great Expectations, Pipeline Monitoring
├── 📂 08_Soft_Skills/                    # Komunikasi Stakeholder, Incident Response
├── 📂 09_Projects_to_Build/              # ELT Pipeline, Streaming Pipeline
├── 📂 10_Learning_Resources/             # Buku, Course, Sertifikasi
├── 📂 11_Data_Ingestion/                 # CSV→DB, DB→DB, Large Data Handling
├── 📂 sql-masterclass/                   # Danny Ma's SQL Course (EN + ID)
├── 📂 web/                               # FastAPI Learning Hub (jalankan sendiri!)
├── 📄 roadmap_data_engineer.md           # Roadmap belajar
└── 📄 interview_preparation.md           # Persiapan wawancara + studi kasus
```

---

## 🗺️ Learning Path (11 Modul)

Setiap modul terdiri dari **penjelasan teori** (`penjelasan.md`) + **kode praktik** yang bisa langsung dijalankan.

### 🔹 01. Programming Fundamentals
| Topik | File | Deskripsi |
|-------|------|-----------|
| SQL Dasar & Lanjutan | `sql/basic_sql.sql`, `sql/advanced_sql.sql` | DDL, DML, JOIN, Window Functions, CTE |
| Shell Scripting | `shell_scripting/etl_pipeline.sh` | ETL pipeline bash lengkap dengan logging & notifikasi |

### 🔹 02. Databases & Storage
| Topik | File | Deskripsi |
|-------|------|-----------|
| PostgreSQL | `relational/postgresql_basics.sql` | UUID, JSONB, Indexing, Stored Procedures |
| MongoDB | `nosql/mongodb_basics.js` | CRUD, Aggregation Pipeline, Change Streams |
| Snowflake | `data_warehouse/snowflake_basics.sql` | Time Travel, Tasks, Streams |

### 🔹 03. Big Data Technologies
| Topik | File | Deskripsi |
|-------|------|-----------|
| Apache Spark | `spark_basics.py` | PySpark, DataFrame, SQL, Partitions |
| Apache Kafka | `kafka_producer_consumer.py` | Producer, Consumer, Key-based Partitioning |
| Apache Airflow | `airflow_dag.py` | DAG, XCom, Retry, Alert |

### 🔹 04. Cloud Platforms
| Topik | File | Deskripsi |
|-------|------|-----------|
| AWS | `aws_s3_glue.py` | S3, Glue Jobs, Lambda, Redshift |

### 🔹 05. Data Pipeline & Architecture
| Topik | File | Deskripsi |
|-------|------|-----------|
| Medallion Architecture | `data_lakehouse/medallion_architecture.sql` | Bronze → Silver → Gold (Delta Lake) |
| Star Schema | `data_modeling/star_schema.sql` | Fact & Dimension Tables dengan SCD Type 2 |

### 🔹 06. Data Engineering Tools
| Topik | File | Deskripsi |
|-------|------|-----------|
| dbt | `dbt/dbt_basics.sql` | Staging → Mart, Automated Testing |
| Docker Compose | `docker-compose_pipeline.yml` | Full stack: Postgres + Spark + Kafka + Airflow + MinIO |
| Terraform | `terraform_aws_infra.tf` | S3 Data Lake, IAM, Redshift, VPC |

### 🔹 07. Monitoring & Observability
| Topik | File | Deskripsi |
|-------|------|-----------|
| Data Quality | `great_expectations_check.py` | Expectations, Validation, Suites |
| Pipeline Monitoring | `pipeline_monitoring.py` | Metrics, Slack Alert, SLO Tracking |

### 🔹 08. Soft Skills
| Topik | File | Deskripsi |
|-------|------|-----------|
| Komunikasi | `stakeholder_communication.md` | Teknik komunikasi dengan stakeholder teknis & non-teknis |
| Incident Response | `incident_runbook.md` | Runbook SEV1/2/3 lengkap |

### 🔹 09. Projects to Build
| Proyek | File | Stack |
|--------|------|-------|
| ELT Pipeline | `elt_pipeline.py` | API → PostgreSQL → SQL Transform |
| Streaming Pipeline | `streaming_pipeline.py` | Kafka → Spark Streaming → Sink |

### 🔹 10. Learning Resources
| Sumber Daya | File |
|-------------|------|
| Buku Rekomendasi | `books/ringkasan_buku.md` |
| Course & Platform | `courses/data_engineering_courses.md` |
| Sertifikasi | `certifications/certification_guide.md` |

### 🔹 11. Data Ingestion
| Metode | File | Cocok Untuk |
|--------|------|-------------|
| CSV → PostgreSQL | `csv_to_postgres.py` | File kecil (<100MB) hingga besar (>1GB) |
| DB → DB | `db_to_db.py` | Transfer antar database |
| Large Data Handling | `large_db_handling.py` | Streaming, Chunking, Parallel Processing |

---

## 🏆 SQL Masterclass + Bonus

### Danny Ma's SQL Masterclass (Bahasa Inggris + Indonesia)

SQL course gratis dari Danny Ma (ODSC Asia Pacific 2021) menggunakan **studi kasus cryptocurrency**.

**[🎯 Mulai Belajar →](sql-masterclass/course-content-id/step1.md)**

| Versi | Lokasi |
|-------|--------|
| 🇬🇧 English | `sql-masterclass/course-content/` |
| 🇮🇩 Indonesia | `sql-masterclass/course-content-id/` |

**Dataset**: `trading.members` (14 anggota) · `trading.prices` (3.404 baris harga) · `trading.transactions` (22.918 transaksi)

```bash
# Setup database (PostgreSQL harus sudah terinstall)
createdb sql_masterclass
psql -d sql_masterclass -f sql-masterclass/data/Postgres/init-postgres.sql
psql -d sql_masterclass -c "\copy trading.transactions FROM 'sql-masterclass/data/transactions.csv' CSV HEADER"

# Mulai belajar
psql -d sql_masterclass
```

### Persiapan Wawancara
File [`interview_preparation.md`](interview_preparation.md) berisi studi kasus arsitektur Medallion + 7 soal wawancara + jawaban detail.

---

## 🌐 Web App Interaktif

Repository ini punya **web app sendiri** untuk belajar lebih interaktif:

```
📂 web/
├── backend/
│   ├── app.py          # FastAPI server
│   └── database.py     # Progress tracking
├── static/
│   ├── css/style.css   # Dark theme UI
│   └── js/app.js       # File tree, search, progress
└── templates/
    └── index.html      # Single-page app
```

### Fitur:
- 📂 **File Tree** — navigasi semua materi
- 🔍 **Search** — cari file dan konten
- ✅ **Progress Tracking** — tandai materi yang sudah selesai
- 📊 **Statistik** — lihat progress belajar

### Jalankan:
```bash
cd web
pip install fastapi uvicorn markdown
python run.py
# Buka http://localhost:8000
```

---

## 🚀 Cara Mulai Belajar

```bash
# 1. Clone repository
git clone https://github.com/adityanuriskandar17/Data.git
cd Data

# 2. Setup database SQL (untuk SQL Masterclass)
createdb sql_masterclass
psql -d sql_masterclass -f sql-masterclass/data/Postgres/init-postgres.sql
psql -d sql_masterclass -c "\copy trading.transactions FROM 'sql-masterclass/data/transactions.csv' CSV HEADER"

# 3. Mulai dari modul 1
code 01_Programming_Fundamentals/penjelasan.md

# 4. Atau langsung dari web app
cd web && python run.py
```

---

## 🧪 Testing & Verifikasi

Beberapa script siap pakai untuk verifikasi pemahaman:

```bash
# Cek SQL Masterclass
psql -d sql_masterclass -c "SELECT * FROM trading.members;"

# Jalankan ETL Pipeline
bash 01_Programming_Fundamentals/shell_scripting/etl_pipeline.sh

# Generate dataset untuk praktik ingestion
python 11_Data_Ingestion/data/generate_data.py
```

---

## 📄 Lisensi

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.

---

<p align="center">
  <b>Selamat Belajar! Jangan lupa ⭐ repo ini jika bermanfaat 🙌</b>
</p>

<p align="center">
  <a href="https://github.com/adityanuriskandar17">GitHub</a>
  ·
  <a href="https://github.com/adityanuriskandar17/Data/issues">Laporkan Masalah</a>
  ·
  <a href="https://github.com/adityanuriskandar17/Data/discussions">Diskusi</a>
</p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:667eea,100:764ba2&height=100&section=footer" />
</p>
