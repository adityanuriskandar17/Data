# Penjelasan: Data Engineering Tools

## 1. dbt (Data Build Tool)

### Apa itu dbt?
dbt adalah alat untuk TRANSFORMASI data di dalam warehouse. Bedanya dengan Python/Spark: dbt cuma pakai SQL!

### Cara Kerja dbt
```
[Data di bronze/silver] → [Model dbt (SQL)] → [Tabel/view di gold]
```

- Kamu tulis SQL SELECT biasa
- dbt akan menjalankan SQL itu dan membuat VIEW atau TABLE
- dbt juga otomatis handle: urutan eksekusi, testing, dokumentasi

### `ref()` function
```sql
SELECT * FROM {{ ref('stg_orders') }}
```
`ref` memberi tahu dbt bahwa model ini bergantung pada model `stg_orders`.
dbt akan:
1. Jalankan `stg_orders` dulu (kalau belum)
2. Ganti `{{ ref('stg_orders') }}` dengan nama tabel yang benar
3. Jalankan model ini

### Testing di dbt
dbt bisa test data secara otomatis:
```
- unique: tidak ada duplikat
- not_null: tidak ada nilai kosong
- accepted_values: hanya nilai tertentu yang diizinkan
- custom test: test sesuai kebutuhan
```

---

## 2. Docker

### Apa itu Docker?
Docker adalah alat untuk "mengemas" aplikasi beserta semua kebutuhannya (OS, library, config) ke dalam container.

### Container vs Virtual Machine
```
VM: [App] [Library] [Guest OS] → [Hypervisor] → [Host OS]
Container: [App] [Library] → [Docker] → [Host OS]
```
Container lebih ringan karena pakai OS host yang sama.

### Kenapa Docker untuk Data Engineering?
- **Konsisten**: "Di laptop saya jalan" bukan masalah lagi
- **Isolasi**: Airflow, Spark, Kafka masing-masing di container sendiri
- **Mudah setup**: cukup `docker-compose up` untuk menjalankan seluruh stack

### docker-compose.yml
File untuk mendefinisikan dan menjalankan banyak container sekaligus.
```yaml
services:
  postgres:    # container 1
    image: postgres:16
  spark:       # container 2
    image: bitnami/spark:3.5
```
Dengan satu perintah: `docker-compose up`, semua service jalan.

---

## 3. Terraform

### Apa itu Terraform?
Alat untuk membuat infrastruktur cloud sebagai KODE.
Daripada klik-klik di AWS console, kamu tulis kode, dan Terraform yang buatkan.

### Contoh:
```hcl
resource "aws_s3_bucket" "data_lake" {
  bucket = "company-data-lake"
}
```
Terraform akan membuat S3 bucket di AWS sesuai konfigurasi.

### Kenapa Penting?
- **Reproducible**: infra bisa dibuat ulang kapan saja
- **Version control**: perubahan infra tercatat di Git
- **Automation**: bisa diintegrasi dengan CI/CD
- **Documentation**: kode Terraform adalah dokumentasi infra

---

## 4. CI/CD (Continuous Integration / Continuous Deployment)

### CI (Continuous Integration)
Setiap kali kamu push kode, otomatis:
1. Di-check kualitasnya (lint)
2. Di-test (pytest)
3. Di-build

### CD (Continuous Deployment)
Setelah CI sukses, otomatis:
1. Deploy ke staging untuk diuji
2. Setelah disetujui, deploy ke production

### Manfaat untuk Data Engineering
- Pipeline baru bisa di-test dulu sebelum production
- Rollback mudah kalau ada masalah
- Kualitas kode terjaga (otomatis di-lint dan di-test)
