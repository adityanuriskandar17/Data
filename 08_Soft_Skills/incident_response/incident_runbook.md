# Incident Response Runbook untuk Data Engineer

## Tujuan
Prosedur standar ketika terjadi masalah pada pipeline data.

## Level Insiden

| Level | Deskripsi | Contoh |
|-------|-----------|--------|
| **SEV1** | Data tidak bisa diakses, semua pipeline down | Database crash, cluster down |
| **SEV2** | Sebagian pipeline gagal, data terlambat | Satu sumber data error |
| **SEV3** | Data quality issue, minor delay | Ada kolom null, format salah |

## Prosedur Response

### Saat Insiden Terjadi

1. **Deteksi**
   - Monitoring alert (Grafana, PagerDuty)
   - Laporan dari user/stakeholder
   - Pipeline failure notification

2. **Triage (5-15 menit)**
   ```
   - Cek dashboard monitoring
   - Cek log pipeline (Airflow logs, aplikasi logs)
   - Cek status service (database, storage, network)
   - Tentukan level insiden
   ```

3. **Komunikasi Awal**
   - Informasi ke tim: "Kami mengetahui ada masalah pada pipeline X.
     Sedang diinvestigasi. Update dalam 30 menit."
   - Buat channel komunikasi khusus jika SEV1

4. **Investigasi & Perbaikan**
   - Rollback jika perubahan terakhir yang menyebabkan error
   - Restart service yang bermasalah
   - Re-run pipeline yang gagal
   - Data backfill jika perlu

5. **Resolusi**
   - Verifikasi pipeline berjalan normal
   - Konfirmasi ke stakeholder
   - Update status di monitoring

6. **Post-Mortem (dalam 1-2 hari)**
   - Dokumentasi kronologi
   - Root cause analysis
   - Action items preventif

## Checklist Cepat

### Pipeline Gagal
- [ ] Cek Airflow log: task mana yang gagal?
- [ ] Cek error message: timeout? connection refused? data corrupt?
- [ ] Cek resource usage: CPU, memory, disk full?
- [ ] Cek source system: API down? DB connection?
- [ ] Cek data quality: ada perubahan format dari source?

### Data Terlambat
- [ ] Cek SLA: berapa lama delay?
- [ ] Prioritaskan data yang paling dibutuhkan
- [ ] Jalankan pipeline manual jika perlu
- [ ] Informasikan estimasi ke stakeholder

### Data Quality Issue
- [ ] Isolate data yang bermasalah
- [ ] Backfill dengan data yang benar
- [ ] Update data quality checks
- [ ] Informasikan stakeholder yang terdampak
