# Penjelasan: Database & Storage

## 1. Jenis Database

### Relational Database (PostgreSQL, MySQL)
- Data disimpan dalam tabel (baris & kolom), seperti Excel
- Ada hubungan (relation) antar tabel pakai foreign key
- Pakai SQL untuk query
- Cocok untuk: data transaksional, data yang terstruktur rapi

### NoSQL Database (MongoDB, Cassandra)
- Data tidak harus dalam tabel
- MongoDB: dokumen JSON fleksibel
- Cassandra: kolom lebar, cocok untuk data time-series
- Cocok untuk: data yang tidak terstruktur, skalabilitas tinggi

### Data Warehouse (Snowflake, BigQuery, Redshift)
- Khusus untuk analisis data dalam jumlah besar
- Optimasi untuk SELECT dan aggregasi, bukan update
- Cocok untuk: laporan bisnis, dashboard, analitik

---

## 2. PostgreSQL

### Primary Key
```sql
customer_id SERIAL PRIMARY KEY
```
- `SERIAL`: otomatis mengisi angka (1, 2, 3, ...)
- `PRIMARY KEY`: nilai unik yang mengidentifikasi setiap baris

### Foreign Key
```sql
customer_id INT REFERENCES customers(customer_id)
```
- Menghubungkan tabel orders ke tabel customers
- Memastikan tidak ada pesanan dari pelanggan yang tidak ada

### Index
```sql
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
```
Database tanpa index membaca SEMUA baris untuk mencari data (full scan).
Database dengan index langsung tahu di mana data berada (seperti indeks buku).

### View vs Materialized View
- **View**: query tersimpan, data selalu terbaru, tapi lambat jika query berat
- **Materialized View**: hasil query disimpan sebagai tabel, cepat, tapi perlu di-refresh

---

## 3. MongoDB

### Document Database
- Data disimpan sebagai dokumen JSON
- Tidak perlu schema tetap seperti SQL
- Collection = kumpulan dokumen (seperti tabel di SQL)

### Query MongoDB vs SQL
| SQL | MongoDB |
|-----|---------|
| `SELECT * FROM logs` | `db.logs.find()` |
| `WHERE level = 'ERROR'` | `{ level: "ERROR" }` |
| `GROUP BY level` | `{ $group: { _id: "$level" } }` |
| `ORDER BY date DESC` | `sort({ date: -1 })` |

---

## 4. Snowflake (Data Warehouse)

### Warehouse
Di Snowflake, "warehouse" adalah sumber daya compute (CPU/RAM) untuk menjalankan query. Bisa di-start/stop otomatis untuk hemat biaya.

### Stage
Tempat penyimpanan file sementara sebelum dimuat ke tabel. Bisa di cloud (S3, GCS) atau internal Snowflake.

### Time Travel
Fitur untuk melihat data di masa lalu - seperti "undo" untuk data.
Berguna untuk: recovery data yang terhapus, audit, analisis perubahan.

### Clustering
Snowflake otomatis mengelompokkan data berdasarkan kolom tertentu untuk mempercepat query.

---

## 5. OLTP vs OLAP

| Aspek | OLTP | OLAP |
|-------|------|------|
| Fungsi | Transaksi harian | Analisis data |
| Contoh | Pesanan, login | Laporan bulanan |
| Banyak baris | Sedikit per query | Jutaan per query |
| Tabel | Normalisasi (3NF) | Denormalisasi (Star) |
| Index | Banyak | Sedikit |
| User | Pelanggan, kasir | Analis, Manager |

### Star Schema
- **Fact table** (tengah): data kejadian/transaksi dengan angka-angka
- **Dimension tables** (bintang): data deskriptif seperti nama, tanggal, kategori
- Bentuknya seperti bintang karena fact di tengah, dimensi di sekeliling
