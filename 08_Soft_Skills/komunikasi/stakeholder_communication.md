# Komunikasi Stakeholder untuk Data Engineer

## 1. Siapa Stakeholder Data Engineer?

| Stakeholder | Kebutuhan | Bahasa yang Dipahami |
|-------------|-----------|---------------------|
| **Data Analyst / BI** | Data tersedia tepat waktu, akurat | SQL, tabel, dashboard |
| **Data Scientist** | Feature engineering, data bersih | Python, statistik, ML pipelines |
| **Product Manager** | Timeline, prioritas, SLA | Bisnis, tanggal, impact |
| **Engineering Manager** | Arsitektur, scalability, cost | Infrastruktur, performa |
| **C-Level** | ROI, data-driven decisions | Revenue, cost, growth |

## 2. Prinsip Komunikasi Efektif

### a. Ketika Ada Masalah Data
```
Jangan:
"Pipeline-nya error karena ada null pointer exception di Spark job."

Lebih baik:
"Data order hari ini akan terlambat ~2 jam karena ada gangguan teknis.
Tim sudah bekerja untuk memperbaikinya. Estimasi selesai jam 11:00."
```

### b. Ketika Menjelaskan Teknis ke Non-Teknis
```
Jangan:
"Kita perlu migrate dari ETL ke ELT karena transformation latency 
lebih rendah dengan MPP architecture."

Lebih baik:
"Kita akan mengubah cara memproses data agar lebih cepat dan fleksibel.
Data akan langsung masuk, baru diproses sesuai kebutuhan. Hasilnya,
laporan bisa tersedia 30 menit lebih cepat."
```

### c. Memberikan Estimasi
- Selalu tambahkan buffer (estimated time x 1.5 - 2x)
- Bedakan: "waktu pengerjaan" vs "waktu tunggu approval/deploy"
- Update progress secara proaktif (jangan menunggu ditanya)

## 3. Meeting yang Efektif

### Daily Standup (15 menit)
- Apa yang dikerjakan kemarin?
- Yang akan dikerjakan hari ini?
- Ada blocker?

### Sprint Planning
- Breakdown task teknis ke subtask yang bisa diestimasi
- Prioritaskan data quality dan reliability

### Post-Mortem (setelah insiden)
1. Kronologi kejadian
2. Root cause
3. Dampak
4. Action items preventif
5. Timeline perbaikan

## 4. Dokumentasi
- Tulis README untuk setiap pipeline
- Data dictionary untuk semua tabel
- Runbook untuk incident response
- Pastikan dokumentasi selalu up-to-date
