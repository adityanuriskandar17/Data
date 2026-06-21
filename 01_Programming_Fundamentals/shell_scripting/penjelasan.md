# Penjelasan: Shell Scripting untuk Data Engineering

## 1. Apa itu Shell Script?
Shell script adalah kumpulan perintah Linux yang ditulis dalam file `.sh` dan bisa dijalankan otomatis. Seperti daftar instruksi untuk komputer.

## 2. Shebang (`#!/bin/bash`)
Baris paling atas. Memberi tahu sistem: "Gunakan program `bash` untuk menjalankan script ini."

## 3. Variabel
```bash
DB_HOST="localhost"
echo "Host: $DB_HOST"
```
- Membuat kotak penyimpanan bernama `DB_HOST` dengan isi `"localhost"`
- `$DB_HOST` untuk mengambil isinya
- Gunakan huruf BESAR untuk variabel (konvensi)

## 4. Kondisional (if)
```bash
if [ -d "$BACKUP_DIR" ]; then
    echo "Directory sudah ada"
else
    mkdir -p "$BACKUP_DIR"
    echo "Directory dibuat"
fi
```

**Cara baca:**
- `if [ -d ... ]` = JIKA direktori sudah ada
- `then` = MAKA lakukan ini
- `else` = KALAU TIDAK, lakukan ini
- `fi` = selesai (if dibalik)

**Operator yang sering dipakai:**
| Operator | Arti |
|----------|------|
| `-d file` | Apakah file adalah directory? |
| `-f file` | Apakah file adalah file biasa? |
| `-z string` | Apakah string kosong? |
| `string1 = string2` | Apakah sama? |

## 5. Perulangan (for)
```bash
for table in customers orders products; do
    echo "Memproses: $table"
done
```

**Artinya:** Untuk setiap nilai dalam daftar `customers orders products`, lakukan perintah di dalamnya.

## 6. Exit Code
```bash
if pg_dump ...; then
    echo "Sukses"
else
    echo "Gagal"
    exit 1
fi
```

Setiap perintah Linux mengembalikan kode:
- `0` = sukses
- `1` = gagal

Script kita bisa cek: kalau `pg_dump` sukses (kode 0), laporan sukses. Kalau gagal (kode ≠ 0), laporan gagal.

## 7. Fungsi
```bash
send_notification() {
    local message=$1
    curl -X POST ... -d "{\"text\": \"$message\"}"
}
```

- `send_notification` adalah nama fungsi
- `$1` adalah parameter/argumen pertama yang diberikan saat fungsi dipanggil
- `local` artinya variabel hanya berlaku di dalam fungsi

## 8. Redirection
```bash
echo "Error" >&2   # kirim ke stderr (error)
echo "Info" >> log.txt  # tambahkan ke file (>> = append)
```

- `>` = tulis ulang file
- `>>` = tambahkan ke file
- `>&2` = kirim ke error stream

## 9. Cron Job (Penjadwalan)
```bash
# 0 2 * * * /home/user/script.sh
```
Format: `menit jam tanggal bulan hari_perintah`
- `0 2 * * *` = setiap jam 2 pagi
- `*/30 * * * *` = setiap 30 menit
