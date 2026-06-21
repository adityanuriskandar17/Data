# Penjelasan: Big Data Technologies

## 1. Kenapa Perlu Big Data Tools?
Database biasa (PostgreSQL, MySQL) sudah cukup untuk jutaan baris. Tapi kalau sudah MILYARAN baris (terabyte data), perlu alat khusus:
- **Spark**: proses data di banyak komputer sekaligus
- **Kafka**: mengalirkan data real-time antar sistem
- **Airflow**: menjadwalkan dan memonitor pipeline

## 2. Apache Spark

### Spark bekerja dengan "distribusi"
Bayangkan punya 1 file besar (100 GB) dan 10 komputer. Spark akan:
1. Memotong file jadi 10 bagian (masing-masing 10 GB)
2. Mengirim 1 bagian ke setiap komputer
3. Semua komputer bekerja BERSAMAAN
4. Menggabungkan hasilnya

Ini yang disebut **distributed computing**.

### DataFrame
Di Spark, data disebut DataFrame. Mirip dengan pandas DataFrame, tapi tersebar di banyak komputer.
```python
df = spark.read.csv("file.csv")  # file dibaca oleh semua komputer
df.groupBy("kolom").sum()        # semua komputer kerja bareng
```

### Lazy Evaluation
Spark tidak langsung menjalankan perintah. Dia mencatat dulu semua perintah, baru dijalankan sekaligus ketika diminta hasilnya (seperti `show()` atau `write`).
Ini membuat Spark bisa optimize urutan eksekusi.

### Partition
Data di Spark dibagi menjadi partisi (potongan). Setiap partisi diproses oleh 1 CPU.
```python
df.repartition(10)  # bagi data jadi 10 partisi
```
Lebih banyak partisi = lebih paralel, tapi ada overhead komunikasi.

---

## 3. Apache Kafka

### Kafka seperti "pos kantor" untuk data
- **Producer**: pengirim surat (aplikasi yang mengirim data)
- **Topic**: alamat tujuan (seperti: "pesanan-masuk")
- **Partition**: antrian di dalam alamat (biar bisa terima banyak surat)
- **Consumer**: penerima surat (aplikasi yang memproses data)
- **Broker**: kantor posnya (server Kafka)

### Cara Kerja
```
Producer → [Topic: "orders"] → Consumer
              (Partition 0)
              (Partition 1)
              (Partition 2)
```

### Kenapa Kafka?
- **Real-time**: data bisa diproses dalam milidetik
- **Tahan lama**: data disimpan di disk, tidak hilang
- **Skalabel**: bisa tambah partition untuk lebih banyak data
- **Decouple**: pengirim dan penerima tidak perlu tahu satu sama lain

### Offset
Setiap pesan di Kafka punya nomor (offset). Consumer ingat offset terakhir yang sudah dibaca.
Jika consumer mati, saat hidup lagi dia lanjut dari offset terakhir, bukan dari awal.

---

## 4. Apache Airflow

### Airflow seperti "asisten pribadi" untuk pipeline
Kamu bisa bilang ke Airflow:
- "Setiap jam 2 pagi, jalankan script backup"
- "Kalau backup selesai, baru jalankan transformasi"
- "Kalau transformasi gagal, coba ulang 3 kali"
- "Kalau tetap gagal, kirim email ke tim"

### DAG (Directed Acyclic Graph)
DAG adalah kumpulan task dengan urutan dependensi.
- **Directed**: urutannya satu arah (A → B → C)
- **Acyclic**: tidak boleh ada putaran (A → B → A tidak boleh)
- **Graph**: kumpulan task yang saling terhubung

### Task
Satu unit pekerjaan. Bisa:
- Menjalankan perintah bash (`BashOperator`)
- Menjalankan Python (`PythonOperator`)
- Copy data (`PostgresOperator`)
- Dan masih banyak lagi

### XCom
Cara task mengirim data ke task lain.
```python
# Task A mengirim file_path
return file_path  # otomatis masuk XCom

# Task B menerima
file_path = context["ti"].xcom_pull(task_ids="extract_data")
```
