# Penjelasan: Soft Skills untuk Data Engineer

## 1. Kenapa Soft Skills Penting?
Data Engineer tidak cuma kerja sendiri ngoding. Kita harus:
- Ngomong sama **Data Analyst**: butuh data apa?
- Ngomong sama **Data Scientist**: fitur apa yang diperlukan?
- Ngomong sama **Manager**: kapan selesai? kenapa lambat?
- Ngomong sama **Bisnis**: apa yang bisa di-improve?

## 2. Komunikasi Efektif

### Terjemahkan teknis ke bahasa bisnis
**Salah:** "Pipeline kita error karena Spark job-nya OOM."
**Benar:** "Ada gangguan teknis, data akan terlambat 1 jam. Tim sedang perbaiki."

### Prinsip: Problem → Impact → Solusi → Timeline
1. **Problem**: apa yang terjadi (jelaskan SEDERHANA)
2. **Impact**: siapa yang terdampak dan bagaimana
3. **Solusi**: apa yang dilakukan untuk memperbaiki
4. **Timeline**: kapan selesai

## 3. Incident Response

### Level Insiden
- **SEV1**: semua mati, semua panik → langsung kerjakan, liburkan semua
- **SEV2**: sebagian mati → prioritaskan, tapi tidak perlu semua orang
- **SEV3**: masalah kecil → masuk backlog

### Golden Rule Incident Response
1. **Komunikasikan dulu** ("Kami tahu ada masalah, sedang diinvestigasi")
2. **Perbaiki** (diagnosa, rollback, restart)
3. **Verifikasi** (pastikan benar-benar normal)
4. **Post-mortem** (pelajari kenapa terjadi, cegah terulang)

### Post-mortem (Tanpa Menyalahkan)
Bukan mencari siapa yang salah, tapi:
- Apa yang terjadi? (kronologi)
- Kenapa bisa terjadi? (root cause)
- Bagaimana mencegah? (action items)
