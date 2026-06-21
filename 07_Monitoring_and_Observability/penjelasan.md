# Penjelasan: Monitoring & Observability

## 1. Kenapa Monitoring Penting?
Di production, pipeline bisa gagal kapan saja:
- Source API tiba-tiba mati
- Database kehabisan disk
- Data tiba-tiba berubah format

Kita perlu TAHU sebelum user/stakeholder yang lapor.

---

## 2. Data Quality (Great Expectations)

### Apa itu Data Quality?
Memastikan data yang kita proses benar dan layak pakai. Contoh cek:
- **Tidak null**: kolom penting harus selalu terisi
- **Range wajar**: amount antara 0 - 1 juta
- **Format benar**: email harus ada @ dan .
- **Unik**: tidak ada order_id duplikat

### Great Expectations
Library Python untuk validasi data quality secara otomatis.
```python
dataset.expect_column_values_to_not_be_null("order_id")
dataset.expect_column_values_to_be_between("amount", 0, 1000000)
```

Setiap validasi disebut "expectation". Kumpulan expectations disebut "expectation suite".

---

## 3. Pipeline Monitoring

### Metrics yang Dipantau
| Metrik | Arti | Alarm Kalau |
|--------|------|-------------|
| Duration | Waktu eksekusi | > threshold normal |
| Rows Read | Baris dibaca | Tiba-tiba turun drastis |
| Error Count | Jumlah error | > 0 |
| Success Rate | Persentase sukses | < 99.9% |
| Throughput | Baris/detik | Turun signifikan |

### Alerting
- **Slack/Email**: notifikasi ke tim
- **PagerDuty**: untuk insiden kritis (bisa telpon)
- **Auto-healing**: coba ulang otomatis kalau gagal

---

## 4. SLI / SLO

- **SLI** (Service Level Indicator): metrik yang diukur
  - Contoh: "persentase pipeline yang sukses"
- **SLO** (Service Level Objective): target yang ingin dicapai
  - Contoh: "99.9% pipeline harus sukses dalam sebulan"

Kalau SLO tidak terpenuhi, berarti perlu perbaikan.
