# Penjelasan: Proyek Data Engineering

## Proyek 1: ELT Pipeline

### Arsitektur
```
[API/Source] → [Extract dengan Python] → [Load ke PostgreSQL (staging)] → [Transform dengan SQL] → [Gold tables]
```

### Cara Kerja
1. **Extract**: Ambil data dari REST API menggunakan `requests.get()`
2. **Load**: Langsung simpan data mentah ke PostgreSQL dengan `df.to_sql()`
3. **Transform**: Jalankan SQL di PostgreSQL untuk membersihkan dan mengagregasi data

### Kenapa ELT (bukan ETL)?
- Data mentah tetap tersimpan kalau perlu diolah ulang
- SQL lebih mudah ditulis dan di-debug
- PostgreSQL cukup kuat untuk transformasi

---

## Proyek 2: Streaming Pipeline

### Arsitektur
```
[Producer] → [Kafka Topic: "orders"] → [Spark Streaming] → [PostgreSQL / Console]
```

### Alur Data
1. **Producer**: Script Python generate data order random, kirim ke Kafka setiap detik
2. **Kafka**: Menerima dan menyimpan pesan, bisa dibaca oleh banyak consumer
3. **Spark Streaming**: Membaca pesan dari Kafka secara real-time, melakukan agregasi per menit
4. **Sink**: Menulis hasil ke console (testing) atau ke database (production)

### Key Concepts
- **Real-time processing**: data diproses dalam hitungan detik (bukan jam)
- **Window**: agregasi per jendela waktu (misal: penjualan per 1 menit)
- **Watermark**: menangani data yang datang terlambat
