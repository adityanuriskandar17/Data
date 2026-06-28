# 🔗 JOIN Itu Sebenarnya Apa Sih?

---

## 🧠 Akar Masalah Pusing

Kebanyakan orang pusing soal JOIN karena **ngelihat query sebagai teks**, bukan sebagai **gerakan data**.

> **SQL itu naratif, bukan matematika.** Kamu harus bayangin "data bergerak", bukan "huruf dicocokin".

---

## 🎬 JOIN = MENGEPEL 2 MEJA

Bayangin kamu punya **2 meja**:

```
MEJA A (transactions)              MEJA B (members)
┌──────┬────────┬──────────┐      ┌──────┬──────────┬──────┐
│ id   │ member │ tipe     │      │ id   │ nama     │ kota │
├──────┼────────┼──────────┤      ├──────┼──────────┼──────┤
│ 1    │ c4ca   │ BUY      │      │ c4ca │ Rina     │ Jkt  │
│ 2    │ c81e   │ SELL     │      │ c81e │ Budi     │ Bdg  │
│ 3    │ xyz   │ SELL     │      │ abc  │ Sari     │ Sby  │
└──────┴────────┴──────────┘      └──────┴──────────┴──────┘
```

JOIN = **ambil 2 meja ini, gabung jadi 1 meja baru**.

---

## 1️⃣ INNER JOIN — Yang Cocok Doang

**Perintah:** "Gabungin 2 meja, tapi **cuma baris yang cocok** di kiri dan kanan"

```sql
FROM transactions
INNER JOIN members ON transactions.member = members.id
```

Cara kerja:
```
MEJA A                        MEJA B
┌────────┬────────┐          ┌──────┬──────────┐
│ member │ tipe   │          │ id   │ nama     │
├────────┼────────┤          ├──────┼──────────┤
│ c4ca   │ BUY    │──cocok──│ c4ca │ Rina     │ ✓
│ c81e   │ SELL   │──cocok──│ c81e │ Budi     │ ✓
│ xyz    │ SELL   │──  ❌  │ abc  │ Sari     │ ← xyz & abc gak cocok
└────────┴────────┘          └──────┴──────────┘

HASIL:
┌────────┬────────┬──────────┐
│ member │ tipe   │ nama     │
├────────┼────────┼──────────┤
│ c4ca   │ BUY    │ Rina     │ ← ada di 2 meja
│ c81e   │ SELL   │ Budi     │ ← ada di 2 meja
└────────┴────────┴──────────┘
```

> INNER JOIN itu **orang yang dateng ke 2 acara** (ultah Rina + reuni Budi).

---

## 2️⃣ LEFT JOIN — Yang Kiri Utama

**Perintah:** "Gabungin 2 meja, **SEMUA baris dari meja KIRI tetap muncul**. Data meja kanan diisi kalau cocok, kalau gak cocok dikosongin (NULL)."

```sql
FROM transactions        ← INI MEJA KIRI
LEFT JOIN members        ← INI MEJA KANAN
  ON transactions.member = members.id
```

Proses:
```
LANGKAH 1 — Ambil SEMUA dari meja kiri (transactions)
┌────────┬────────┐
│ member │ tipe   │
├────────┼────────┤
│ c4ca   │ BUY    │  ← TETAP MUNCUL
│ c81e   │ SELL   │  ← TETAP MUNCUL  
│ xyz    │ SELL   │  ← TETAP MUNCUL (walau gak cocok!)
└────────┴────────┘

LANGKAH 2 — Tempelin data dari meja kanan (members) kalau cocok
┌────────┬────────┬──────────┐
│ member │ tipe   │ nama     │
├────────┼────────┼──────────┤
│ c4ca   │ BUY    │ Rina     │ ← cocok, dapet nama
│ c81e   │ SELL   │ Budi     │ ← cocok, dapet nama
│ xyz    │ SELL   │ NULL     │ ← TIDAK cocok → dikasih NULL
└────────┴────────┴──────────┘
```

### 🎯 Analogi LEFT JOIN

Kamu dikasih tugas **mendata SEMUA murid di kelas** + nilai ujiannya:

```
ABSEN KELAS (KIRI)                       BUKU NILAI (KANAN)
┌──────────┬────────┐                   ┌──────────┬───────┐
│ nama     │ hadir  │                   │ nama     │ nilai │
├──────────┼────────┤                   ├──────────┼───────┤
│ Adi      │ ✓      │──cocok───────────│ Adi      │ 90    │
│ Budi     │ ✓      │──cocok───────────│ Budi     │ 80    │
│ Caca     │ ✓      │──  ❌           │ Dedi     │ 85    │
│ Dedi     │ ✓      │← DEDII MUNCUL!  │          │       │
└──────────┴────────┘                   └──────────┴───────┘

HASIL LAPORAN (LEFT JOIN):
┌──────────┬────────┬───────┐
│ nama     │ hadir  │ nilai │
├──────────┼────────┼───────┤
│ Adi      │ ✓      │ 90    │
│ Budi     │ ✓      │ 80    │
│ Caca     │ ✓      │ NULL  │ ← gak punya nilai, tapi TETAP MUNCUL
│ Dedi     │ ✓      │ 85    │ ← Dedi muncul karena di kelas (kiri)
└──────────┴────────┴───────┘
```

> **Kiri** = absen kelas → SEMUA murid harus dilaporin, mau punya nilai atau nggak.

---

## ❌ Yang BIKIN BINGUNG

### Mitos 1: "Kiri/kanan di ON itu penting"

```sql
-- INI HASILNYA SAMA PERSIS
FROM A LEFT JOIN B ON A.id = B.id
FROM A LEFT JOIN B ON B.id = A.id
```

> `ON` cuma bilang **"cocokin lewat kolom apa"**. Mau ditulis kiri/kanan, hasilnya SAMA.

### Mitos 2: "LEFT JOIN artinya tabel kiri di ON"

Enggak. LEFT JOIN artinya **tabel yang disebut SEBELUM kata JOIN** itu yang diutamakan.

### Mitos 3: "Paham JOIN = paham query"

Paham JOIN = paham **data bergerak**. Bukan sekadar hafal syntax.

---

## 🧪 Cara Paling Gampang buat Paham

**Jalankan sendiri dan liat bedanya:**

```bash
psql -d sql_masterclass
```

```sql
-- Coba 3 query ini, liat hasilnya
-- 1. INNER JOIN
SELECT m.first_name, t.txn_id
FROM trading.members m
INNER JOIN trading.transactions t ON m.member_id = t.member_id;

-- 2. LEFT JOIN (members di kiri)
SELECT m.first_name, t.txn_id
FROM trading.members m
LEFT JOIN trading.transactions t ON m.member_id = t.member_id;

-- 3. LEFT JOIN (transactions di kiri)
SELECT m.first_name, t.txn_id
FROM trading.transactions t
LEFT JOIN trading.members m ON t.member_id = m.member_id;
```

**Liat bedanya?** Itu dia intinya. Yang manayang disebut di `FROM` itu yang "diutamakan".

---

## 📊 Ringkasan 1 Kalimat

| JOIN | Arti |
|------|------|
| `INNER JOIN` | Ambil **yang cocok aja** dari 2 meja |
| `LEFT JOIN` | **Meja kiri (FROM) TETAP FULL**, meja kanan ngikut kalo cocok |
| `RIGHT JOIN` | Kebalikan LEFT, meja kanan yang full |
| `FULL JOIN` | **2 meja full**, yang gak cocok dikasih NULL |
| `CROSS JOIN` | Semua baris kiri × semua baris kanan |
