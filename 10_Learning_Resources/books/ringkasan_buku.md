# Ringkasan Buku Data Engineering

## 1. Fundamentals of Data Engineering
**Penulis: Joe Reis & Matt Housley**

### Konsep Kunci
- **Data Engineering Lifecycle**: Generation -> Storage -> Ingestion -> Transformation -> Serving
- **Undercurrents**: Security, Data Management, DataOps, Data Architecture, Orchestration, Software Engineering
- **Dimensions of Data**: Source, Frequency, Volume, Velocity, Variety

### Yang Dipelajari
- Perbedaan data engineer vs data scientist vs data analyst
- Memilih teknologi yang tepat berdasarkan use case
- Data architecture patterns (lambda, kappa, medallion)
- Production-grade data pipeline design

---

## 2. Designing Data-Intensive Applications
**Penulis: Martin Kleppmann**

### Konsep Kunci
- **Reliability, Scalability, Maintainability** - tiga pilar sistem data
- **Replication**: single-leader, multi-leader, leaderless
- **Partitioning**: hash-based, range-based, consistent hashing
- **Transactions**: ACID, BASE, distributed transactions
- **Batch Processing**: MapReduce, Spark
- **Stream Processing**: Kafka, exactly-once semantics

### Yang Dipelajari
- Bagaimana database bekerja di balik layar
- Trade-off consistency vs availability (CAP theorem)
- Distributed systems patterns
- Stream processing concepts

---

## 3. The Data Warehouse Toolkit (3rd Edition)
**Penulis: Ralph Kimball**

### Konsep Kunci
- **Dimensional Modeling**: Fact tables + Dimension tables
- **Star Schema vs Snowflake Schema**
- **SCD (Slowly Changing Dimensions)**: Type 0-6
- **Conformed Dimensions**: Dimensi yang digunakan bersama antar fact
- **Bridge Tables**: Untuk relasi many-to-many

### Yang Dipelajari
- Mendesain data warehouse yang benar
- Teknik modeling untuk berbagai industri (retail, finance, healthcare)
- ETL/ELT design patterns

---

## Buku Tambahan

| Judul | Penulis | Fokus |
|-------|---------|-------|
| *Spark: The Definitive Guide* | Bill Chambers & Matei Zaharia | Apache Spark |
| *Kafka: The Definitive Guide* | Neha Narkhede & Gwen Shapira | Apache Kafka |
| *Designing Data Pipelines* | James Densmore | Pipeline design |
| *The Data Engineering Cookbook* | Andreas Kretz | Praktis, berbagai tools |
| *SQL Performance Explained* | Markus Winand | Query optimization |
