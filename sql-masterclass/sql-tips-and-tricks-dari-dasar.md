# 🧠 SQL Dari Dasar Sampai Paham

> **Dibuat untuk yang dari 0 — bahkan yang bilang "aku bodok SQL" bakal ngerti**

---

## 📖 Daftar Isi

1. [SQL Itu Sebenarnya Apa?](#1-sql-itu-sebenarnya-apa)
2. [Database Itu Kayak Apa?](#2-database-itu-kayak-apa)
3. [SELECT — Melihat Data](#3-select--melihat-data)
4. [WHERE — Nyaring Data](#4-where--nyaring-data)
5. [ORDER BY — Ngurutin Data](#5-order-by--ngurutin-data)
6. [GROUP BY — Ngelompokin Data](#6-group-by--ngelompokin-data)
7. [HAVING — Filter buat Kelompok](#7-having--filter-buat-kelompok)
8. [CASE WHEN — Bikin Kolom Baru](#8-case-when--bikin-kolom-baru)
9. [JOIN — Nyambungin Tabel](#9-join--nyambungin-tabel)
10. [Subquery — Query di Dalam Query](#10-subquery--query-di-dalam-query)
11. [CTE — Bikin Query Bertahap](#11-cte--bikin-query-bertahap)
12. [Window Functions — Main Data Tanpa Ngeruntuhin](#12-window-functions--main-data-tanpa-ngeruntuhin)
13. [Flow Diagram Memilih Query](#13-flow-diagram-memilih-query)
14. [Tips Ampuh Biar Gak Pusing](#14-tips-amput-biar-gak-pusing)

---

## 1. SQL Itu Sebenarnya Apa?

**SQL** = **S**tructured **Q**uery **L**anguage

Terjemahan bebasnya: **"Bahasa buat ngomong sama database"**

Gambarin gini:
```
Kamu (manusia)           Database (komputer)
    |                           |
    |   "SELECT * FROM meja"    |
    |-------------------------->|
    |                           |
    |   [data yang kamu mau]    |
    |<--------------------------|
    |                           |
```

SQL itu kayak kamu **ngomong ke komputer** pakai bahasa khusus, dan komputer ngasih data yang kamu minta.

---

## 2. Database Itu Kayak Apa?

**Database** ibarat **lemari arsip** besar.

```
            LEMARI DATABASE
    ┌─────────────────────────────────┐
    │                                 │
    │  📁 Schema "trading"            │
    │  ┌──────────────────────┐       │
    │  │ 📋 Tabel "members"   │       │  <-- ini kayak map berisi data
    │  │ ┌────┬──────┬──────┐│       │
    │  │ │ id │ nama │ kota ││       │  <-- kolom/column
    │  │ ├────┼──────┼──────┤│       │
    │  │ │ 1  │ Adi  │ Jkt  ││       │  <-- baris/row (satu data)
    │  │ │ 2  │ Budi │ Bdg  ││       │
    │  │ └────┴──────┴──────┘│       │
    │  └──────────────────────┘       │
    │                                 │
    │  📁 Tabel "prices"              │
    │  ┌──────────────────────┐       │
    │  │ ticker │ tgl │ harga │       │
    │  ├────────┼─────┼───────┤       │
    │  │ BTC    │ ... │ 500jt │       │
    │  └──────────────────────┘       │
    └─────────────────────────────────┘
```

**Istilah penting:**
- **Tabel** : lemari arsip. Tempat nyimpen data.
- **Kolom** : jenis data (nama, umur, kota).
- **Baris** : satu data lengkap (misal: data si Adi).
- **Schema** : grup dari beberapa tabel.

---

## 3. SELECT — Melihat Data

Ini query paling dasar. Artinya: **"TAMPILIN DATA DARI TABEL INI"**

```sql
SELECT * FROM trading.members;
```

Dibaca: "SELECT semua kolom dari tabel trading punya members"

### 🎯 Analogi

Kamu punya buku telepon. `SELECT * FROM buku_telepon;` = kamu buka buku telepon dan baca SEMUA isinya.

### Variasi SELECT

```sql
-- 1. Ambil semua kolom
SELECT * FROM members;

-- 2. Ambil kolom tertentu aja
SELECT first_name, region FROM members;

-- 3. Ambil tapi batasin jumlahnya
SELECT * FROM members LIMIT 5;

-- 4. Kasih judul baru (alias)
SELECT first_name AS nama_depan FROM members;
```

### 📊 Flow Diagram

```
┌─────────────────────────────────────────────┐
│                                             │
│   SELECT first_name, region                 │
│   → dari tabel members                      │
│   → tampilkan kolom first_name & region     │
│                                             │
└─────────────────────────────────────────────┘
         │
         ▼
┌────────────────────────────┐
│  first_name  │  region     │
├──────────────┼─────────────┤
│  Danny       │  Australia  │
│  Vipul       │  US         │
│  Charlie     │  US         │
│  ...         │  ...        │
└────────────────────────────┘
```

---

## 4. WHERE — Nyaring Data

WHERE = **"KASIH TAU SYARATNYA"**

```sql
SELECT * FROM members WHERE region = 'Australia';
```

Dibaca: "Ambil semua data dari members yang region-nya Australia"

### 🎯 Analogi

Kamu punya keranjang penuh bola warna-warni. Kamu mau ambil **bola merah aja**. WHERE itu kayak kamu bilang "ambil yang warnanya merah aja ya".

### Operator WHERE Paling Sering Dipake

| Operator | Maksud | Contoh |
|----------|--------|--------|
| `=` | Sama dengan | `region = 'US'` |
| `<>` atau `!=` | Tidak sama | `region <> 'US'` |
| `>` | Lebih besar | `harga > 1000` |
| `<` | Lebih kecil | `harga < 500` |
| `>=` | Lebih besar sama dengan | `harga >= 100` |
| `<=` | Lebih kecil sama dengan | `harga <= 50` |
| `BETWEEN` | Di antara | `harga BETWEEN 100 AND 200` |
| `IN` | Termasuk salah satu | `region IN ('US','Asia')` |
| `LIKE` | Mirip / mengandung | `nama LIKE '%dan%'` |
| `IS NULL` | Kosong | `alamat IS NULL` |
| `AND` | Dan (semua harus true) | `region='US' AND umur>20` |
| `OR` | Atau (salah satu true) | `region='US' OR region='Asia'` |

### Contoh WHERE Bertingkat

```sql
SELECT * FROM members 
WHERE region = 'United States' 
  AND first_name LIKE 'A%';
```

Maksudnya: **tampilin semua member dari US yang namanya mulai dari huruf A**.

### 📊 Flow Diagram WHERE

```
┌──────────┐
│  Semua   │
│  Data    │──────┐
└──────────┘      │
                  ▼
         ┌────────────────────┐
         │  WHERE region =    │
         │  'Australia'       │
         │                    │
         │  ✅ Australia      │
         │  ❌ US             │
         │  ❌ India          │
         └────────────────────┘
                  │
                  ▼
         ┌────────────────────┐
         │  HANYA YANG        │
         │  AUSTRALIA         │
         │  yang muncul       │
         └────────────────────┘
```

---

## 5. ORDER BY — Ngurutin Data

**ORDER BY** = **"URUTIN BERDASARKAN..."**

```sql
SELECT * FROM members ORDER BY region;
```

Maksud: "Tampilin semua member, urutin berdasarkan region (A-Z)"

### Jenis Urutan

```sql
-- Urut dari A ke Z (kecil ke besar) → DEFAULT
SELECT * FROM members ORDER BY region ASC;

-- Urut dari Z ke A (besar ke kecil)
SELECT * FROM members ORDER BY region DESC;
```

### 🎯 Analogi

Kamu punya tumpukan kertas nama. `ORDER BY nama ASC` = kamu susun dari A sampai Z. `ORDER BY nama DESC` = kamu susun dari Z sampai A.

---

## 6. GROUP BY — Ngelompokin Data

**GROUP BY** = **"KUMPULIN BERDASARKAN KELOMPOK"**

Biasanya dipasangkan dengan **fungsi agregat** (penjumlah / penghitung).

```sql
SELECT region, COUNT(*) AS jumlah_member
FROM members
GROUP BY region;
```

Hasilnya:

| region | jumlah_member |
|--------|--------------|
| Africa | 1 |
| Asia | 1 |
| Australia | 4 |
| India | 1 |
| United States | 7 |

### 🎯 Analogi

Kamu punya sekantong kelereng warna-warni. `GROUP BY warna` = kamu pisahin kelereng berdasarkan warnanya. Lalu `COUNT(*)` = kamu hitung ada berapa kelereng per warna.

### Fungsi Agregat yang Sering Dipake

| Fungsi | Arti | Contoh |
|--------|------|--------|
| `COUNT(*)` | Hitung jumlah baris | Berapa orang total? |
| `SUM(harga)` | Jumlahkan | Total penjualan |
| `AVG(harga)` | Rata-rata | Harga rata-rata |
| `MIN(harga)` | Nilai terkecil | Harga paling murah |
| `MAX(harga)` | Nilai terbesar | Harga paling mahal |

### 📊 Visual GROUP BY

```
DATA MENTAH:
┌─────────┬────────┐
│ Danny   │ 5rb    │
│ Vipul   │ 3rb    │
│ Danny   │ 2rb    │
│ Vipul   │ 7rb    │
│ Charlie │ 4rb    │
└─────────┴────────┘

GROUP BY nama:
┌─────────┐
│ Danny   │ ─→ 5rb + 2rb = 7rb
│ Vipul   │ ─→ 3rb + 7rb = 10rb
│ Charlie │ ─→ 4rb
└─────────┘
         │
         ▼
┌─────────┬────────────┐
│ nama    │ total_uang │
├─────────┼────────────┤
│ Charlie │ 4rb        │
│ Danny   │ 7rb        │
│ Vipul   │ 10rb       │
└─────────┴────────────┘
```

---

## 7. HAVING — Filter buat Kelompok

**HAVING** = **"FILTER setelah data dikelompokin"**

> 📌 **Bedanya WHERE sama HAVING:**
> - `WHERE` = filter data **sebelum** dikelompokin
> - `HAVING` = filter data **setelah** dikelompokin

```sql
SELECT region, COUNT(*) AS jumlah
FROM members
GROUP BY region
HAVING COUNT(*) > 1;
```

Artinya: "Tampilin region yang jumlah membernya lebih dari 1"

Hasilnya:

| region | jumlah |
|--------|--------|
| Australia | 4 |
| United States | 7 |

(Region yang cuma 1 member kayak Africa, Asia, India gak muncul)

### 🎯 Analogi

Kamu lagi ngelompokin buah per keranjang.
- `WHERE` = kamu buang apel yang busuk SEBELUM masuk keranjang
- `HAVING` = kamu cuma ambil keranjang yang isinya > 5 buah

---

## 8. CASE WHEN — Bikin Kolom Baru

**CASE WHEN** = **"KALAU... MAKA..."**

Bikin kolom baru berdasarkan kondisi tertentu.

```sql
SELECT 
  first_name,
  region,
  CASE 
    WHEN region = 'Australia' THEN 'Lokal'
    ELSE 'Manca Negara'
  AS kategori
FROM members;
```

Hasilnya:

| first_name | region | kategori |
|------------|--------|----------|
| Danny | Australia | Lokal |
| Vipul | United States | Manca Negara |
| Charlie | United States | Manca Negara |
| ... | ... | ... |

### 🎯 Analogi

Kayak kamu ngasih stiker ke orang:
- Kalau orangnya dari Australia → stiker "Lokal"
- Selain itu → stiker "Manca Negara"

### CASE Bertingkat

```sql
SELECT 
  first_name,
  region,
  CASE 
    WHEN region = 'Australia' THEN 'Lokal'
    WHEN region = 'United States' THEN 'Amerika'
    WHEN region = 'Asia' THEN 'Asia'
    ELSE 'Lainnya'
  AS kategori
FROM members;
```

---

## 9. JOIN — Nyambungin Tabel

**JOIN** = **"GABUNGIN 2 TABEL JADI SATU"**

### 🎯 Analogi Paling Gampang

Bayangin kamu punya 2 kertas:

**Kertas 1: Daftar member**
| id_member | nama |
|-----------|------|
| 1 | Danny |
| 2 | Vipul |

**Kertas 2: Daftar transaksi**
| id_member | tgl | jumlah |
|-----------|-----|--------|
| 1 | 1 Jan | 50 |
| 2 | 2 Jan | 30 |

JOIN itu kayak kamu **ngegabungin 2 kertas itu jadi 1**, dicocokkin lewat `id_member`.

```sql
SELECT members.first_name, transactions.txn_date, transactions.quantity
FROM members
JOIN transactions ON members.member_id = transactions.member_id;
```

### 📊 Flow Diagram JOIN

```
┌─────────────────────┐     ┌─────────────────────────┐
│      members        │     │      transactions        │
├─────────────────────┤     ├─────────────────────────┤
│ member_id (kunci)   │     │ member_id (kunci)        │
│ first_name          │     │ txn_date                 │
│ region              │     │ quantity                 │
└──────────┬──────────┘     └──────────┬──────────────┘
           │                           │
           └───────────JOIN────────────┘
                           │
                           ▼
           ┌──────────────────────────────┐
           │         HASILNYA             │
           ├──────────────────────────────┤
           │ first_name │ tgl    │ jumlah │
           ├────────────┼────────┼────────┤
           │ Danny      │ 1 Jan  │ 50     │
           │ Vipul      │ 2 Jan  │ 30     │
           └──────────────────────────────┘
```

### Jenis-Jenis JOIN

Ilustrasi pake lingkaran (Venn Diagram):

```
                     ┌─────┐
         ┌───────────┤ INNER JOIN ├───────────┐
         │           └─────┬────┘             │
         ▼                 │                  ▼
    ┌────────┐      ┌──────────┐       ┌────────┐
    │  LEFT  │      │   INNER  │       │ RIGHT  │
    │  TABLE │      │ ┌──────┐ │       │ TABLE  │
    │ ┌────┐ │      │ │ SAMA │ │       │ ┌────┐ │
    │ │SEMUA│ │      │ │      │ │       │ │SEMUA│ │
    │ └────┘ │      │ └──────┘ │       │ └────┘ │
    └────────┘      └──────────┘       └────────┘
```

### 1. INNER JOIN (Paling Sering Dipake)
Hanya ambil data **yang cocok di 2 tabel**.

```sql
SELECT *
FROM members
INNER JOIN transactions ON members.member_id = transactions.member_id;
```

> Bayangin: 2 orang saling kenalan. Yang gak saling kenal diabaikan.

### 2. LEFT JOIN
**Semua data dari kiri**, data kanan dicocokkin (kalau gak ada jadi NULL).

```sql
SELECT *
FROM members
LEFT JOIN transactions ON members.member_id = transactions.member_id;
```

> Bayangin: Kamu ambil absen semua siswa. Yang pernah bayar ditulis nominalnya, yang belum bayar dikasih tanda "-".

### 3. RIGHT JOIN
**Semua data dari kanan**, data kiri dicocokkin.

```sql
SELECT *
FROM members
RIGHT JOIN transactions ON members.member_id = transactions.member_id;
```

> Kebalikannya LEFT JOIN. Jarang dipake, mending pake LEFT JOIN aja.

### 4. FULL OUTER JOIN
**Semua data dari 2 tabel**, cocokkin yang cocok, sisanya NULL.

```sql
SELECT *
FROM members
FULL OUTER JOIN transactions ON members.member_id = transactions.member_id;
```

> Kayak reuni: semua diundang, yang dateng dicatat, yang gak dateng juga dicatat.

### 5. CROSS JOIN (JOIN Paling Sederhana)
Setiap baris di tabel A dipasangin ke setiap baris di tabel B.

```sql
SELECT *
FROM members
CROSS JOIN transactions;
```

> Bayangin: Kamu punya 3 topi dan 2 baju. Kamu cobain SEMUA kombinasi = 6 gaya.

### 📊 Tabel Kapan Pake JOIN Apa

| Mau-nya | Pake JOIN |
|---------|-----------|
| Data yang cocok di 2 tabel aja | `INNER JOIN` |
| Semua data tabel A + data B yang cocok | `LEFT JOIN` |
| Semua data tabel B + data A yang cocok | `RIGHT JOIN` |
| Semua data dari 2 tabel | `FULL OUTER JOIN` |
| Semua kombinasi (kartesian) | `CROSS JOIN` |

### JOIN 3 Tabel atau Lebih

Bisa aja! Sambungin aja satu-satu.

```sql
SELECT *
FROM members
JOIN transactions ON members.member_id = transactions.member_id
JOIN prices ON transactions.ticker = prices.ticker;
```

---

## 10. Subquery — Query di Dalam Query

**Subquery** = **"QUERY DI DALAM QUERY LAIN"**

```sql
SELECT * 
FROM members
WHERE member_id IN (
  SELECT member_id 
  FROM transactions 
  WHERE quantity > 100
);
```

Maksud: "Cari member yang pernah transaksi lebih dari 100"

### Cara Bacanya

```
LANGKAH 1: Jalankan query DALAM dulu
           → SELECT member_id FROM transactions WHERE quantity > 100
           → hasilnya: ('c81e72', 'eccbc8', ...)

LANGKAH 2: Masukin hasilnya ke query LUAR
           → SELECT * FROM members WHERE member_id IN ('c81e72', 'eccbc8', ...)
```

### 📊 Flow Subquery

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│   SELECT * FROM members WHERE member_id IN (         │
│       ┌─────────────────────────────────────────┐    │
│       │  SELECT member_id                       │    │
│       │  FROM transactions                      │    │
│       │  WHERE quantity > 100                   │    │
│       └────────────┬────────────────────────────┘    │
│                    │                                  │
│                    ▼                                  │
│             hasil: ['c81e72','eccbc8',...]             │
│                    │                                  │
│                    ▼                                  │
│   SELECT * FROM members                               │
│   WHERE member_id IN ['c81e72','eccbc8',...]           │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### Jenis Subquery

```sql
-- Di WHERE (paling sering)
SELECT * FROM tabel WHERE kolom IN (SELECT ...);

-- Di FROM (subquery jadi tabel sementara)
SELECT * FROM (SELECT * FROM members WHERE region = 'US') AS tmp;

-- Di SELECT (bikin kolom baru)
SELECT 
  first_name,
  (SELECT COUNT(*) FROM transactions WHERE member_id = members.member_id) AS total_txn
FROM members;
```

---

## 11. CTE — Bikin Query Bertahap

**CTE** = **C**ommon **T**able **E**xpression

Bikin "tabel sementara" yang bisa dipake di query selanjutnya.

```sql
WITH member_us AS (
  SELECT * FROM members WHERE region = 'United States'
)
SELECT * FROM member_us;
```

### 🎯 Analogi

CTE itu kayak kamu **nulis catatan di kertas tempelan** sebelum ngerjain soal.

```
Kertas tempelan:
┌────────────────────┐
│  member_us =       │
│  (SELECT * FROM    │
│   members WHERE    │
│   region = 'US')   │
└────────────────────┘
         │
         ▼
┌────────────────────┐
│  SELECT * FROM     │
│  member_us         │
│  → pake kertas     │
│    tempelan tadi   │
└────────────────────┘
```

### CTE vs Subquery

```sql
-- ❌ Subquery (ribet dibaca kalau panjang)
SELECT * FROM members WHERE member_id IN (
  SELECT member_id FROM transactions WHERE quantity > (
    SELECT AVG(quantity) FROM transactions
  )
);

-- ✅ CTE (jauh lebih rapi)
WITH rata_rata AS (
  SELECT AVG(quantity) AS avg_qty FROM transactions
),
transaksi_besar AS (
  SELECT member_id FROM transactions 
  WHERE quantity > (SELECT avg_qty FROM rata_rata)
)
SELECT * FROM members WHERE member_id IN (SELECT member_id FROM transaksi_besar);
```

## 12. Window Functions — Main Data Tanpa Ngeruntuhin

**Window Function** = **NGITUNG SESUATU TAPI BARIS ASLINYA GAK ILANG**

Bedanya sama GROUP BY: GROUP BY ngeruntuhin baris jadi kelompok, Window Function gak.

```sql
SELECT 
  first_name,
  region,
  COUNT(*) OVER (PARTITION BY region) AS jumlah_per_region
FROM members;
```

Hasilnya:

| first_name | region | jumlah_per_region |
|------------|--------|------------------|
| Danny | Australia | 4 |
| Ben | Australia | 4 |
| Pavan | Australia | 4 |
| Sonia | Australia | 4 |
| Vipul | United States | 7 |
| ... | United States | 7 |

### 📊 Perbedaan GROUP BY vs Window

```
DATA:   Danny(AUS), Ben(AUS), Vipul(US), Charlie(US)

GROUP BY region:
┌───────────┬────────┐
│ Australia │ 2      │  ← barisnya cuma 2
│ US        │ 2      │
└───────────┴────────┘

Window Function:
┌────────┬────┬───────────────┐
│ Danny  │ AUS│ 2 (total AUS) │  ← baris tetap 4
│ Ben    │ AUS│ 2 (total AUS) │
│ Vipul  │ US │ 2 (total US)  │
│ Charlie│ US │ 2 (total US)  │
└────────┴────┴───────────────┘
```

### 🎯 Analogi

GROUP BY kayak kamu ngelompokin murid per kelas, terus ditulis "Kelas A: 30 murid" — data murid per orang hilang.

Window Function kayak kamu tulis "Kelas A: 30 murid" di samping NAMA setiap murid — data per orang tetap ada.

### Window Functions Paling Sering Dipake

```sql
-- 1. ROW_NUMBER() → kasih nomor urut per grup
SELECT 
  first_name,
  region,
  ROW_NUMBER() OVER (PARTITION BY region ORDER BY first_name) AS urutan
FROM members;

-- 2. RANK() → ranking, nilai sama dapet rank sama
SELECT 
  ticker,
  price,
  RANK() OVER (ORDER BY price DESC) AS peringkat
FROM prices;

-- 3. LAG() → liat baris SEBELUMNYA
SELECT 
  market_date,
  price,
  LAG(price) OVER (ORDER BY market_date) AS harga_kemarin
FROM prices;

-- 4. LEAD() → liat baris SETELAHNYA
SELECT 
  market_date,
  price,
  LEAD(price) OVER (ORDER BY market_date) AS harga_besok
FROM prices;
```

---

## 13. Flow Diagram Memilih Query

```
KAMU MAU NGAPAIN?
        │
        ▼
┌─────────────────────────────┐
│ "Mau lihat data doang"      │────→ SELECT ... FROM ...
│                             │
│ "Mau lihat yang tertentu"   │────→ ... WHERE ... 
│                             │
│ "Mau ngurutin"              │────→ ... ORDER BY ...
│                             │
│ "Mau ngehitung per kelompok"│────→ ... GROUP BY ... 
│                             │
│ "Mau filter kelompok"       │────→ ... HAVING ...
│                             │
│ "Mau bikin kolom baru"      │────→ CASE WHEN ... THEN ...
│                             │
│ "Mau gabung 2 tabel"        │────→ ... JOIN ...
│                             │
│ "Query ribet, bikin rapih"  │────→ WITH ... AS (...)
│                             │
│ "Hitung per grup,           │
│  tapi baris jangan ilang"   │────→ ... OVER (PARTITION BY ...)
│                             │
│ "Cari sesuatu pake hasil    │
│  query lain"                │────→ ... IN (SELECT ...)
└─────────────────────────────┘
```

---

## 14. Tips AmpuH Biar Gak Pusing

### 🔥 Golden Rules

1. **SELECT dulu satu kolom**, jangan langsung SELECT *
2. **Kerjain bertahap**: WHERE dulu, baru GROUP BY, baru HAVING
3. **Kalau pusing, pecah jadi CTE**
4. **Inget urutan eksekusi SQL** (ini penting banget):

```
URUTAN EKSEKUSI SQL:
                              │
    FROM / JOIN     ──→ 1    │  (ambil dulu sumber datanya)
    WHERE           ──→ 2    │  (filter data mentah)
    GROUP BY        ──→ 3    │  (kelompokin)
    HAVING          ──→ 4    │  (filter kelompok)
    SELECT          ──→ 5    │  (pilih kolom yang ditampilin)
    ORDER BY        ──→ 6    │  (urutin hasil akhir)
    LIMIT           ──→ 7    │  (batasin jumlah)
                              │
```

> ⚠️ Ini penting: WHERE jalan SEBELUM GROUP BY. Makanya WHERE gak bisa pake hasil agregat kayak `SUM()`.

### 💡 Contoh Penerapan Urutan

```sql
-- Kamu tulis:
SELECT region, COUNT(*) AS jumlah    
FROM members                           
WHERE first_name != 'Danny'            
GROUP BY region                        
HAVING COUNT(*) > 1                    
ORDER BY jumlah DESC;                  

-- Tapi komputer jalannya:
-- 1. FROM members                    → ambil semua data members
-- 2. WHERE first_name != 'Danny'     → buang baris yang namanya Danny
-- 3. GROUP BY region                 → kelompokin per region
-- 4. HAVING COUNT(*) > 1            → ambil kelompok yang > 1 orang
-- 5. SELECT region, COUNT(*)         → tampilin region dan jumlahnya
-- 6. ORDER BY jumlah DESC            → urutin dari terbanyak
```

### 🎯 Analogi Urutan Eksekusi

Bayangin kamu mau bikin laporan penjualan:

| Langkah | SQL | Analogi |
|---------|-----|---------|
| 1 | `FROM` | Ambil semua nota penjualan dari laci |
| 2 | `WHERE` | Buang nota yang tanggalnya bukan bulan ini |
| 3 | `GROUP BY` | Kelompokin nota per produk |
| 4 | `HAVING` | Ambil produk yang laku > 10 aja |
| 5 | `SELECT` | Tulis nama produk dan jumlah terjual |
| 6 | `ORDER BY` | Urutin dari yang paling laku |
| 7 | `LIMIT` | Ambil top 5 aja |

### ⚡ Trik Cepat

```sql
-- Cek isi tabel (5 baris pertama)
SELECT * FROM nama_tabel LIMIT 5;

-- Cek jumlah baris
SELECT COUNT(*) FROM nama_tabel;

-- Cek struktur tabel (di psql)
\d nama_tabel

-- Cek kolom unik di suatu kolom
SELECT DISTINCT nama_kolom FROM nama_tabel;

-- Debug: jalanin query dalem dulu sendiri
-- SELECT * FROM ... → cek hasilnya bener apa enggak
-- Baru dipake di query utama
```

### 📝 Checklist Sebelum Jalanin Query

```
☐ Nama tabel bener? (cek pake \d atau SELECT * FROM ... LIMIT 1)
☐ Nama kolom bener? (jangan sampe salah ketik)
☐ WHERE nya bener? (coba SELECT dulu baru WHERE)
☐ JOIN pake kolom yang bener? (cek nama kolom di 2 tabel)
☐ GROUP BY udah sesuai? (semua kolom di SELECT harus ada di GROUP BY kecuali agregat)
☐ Urutan WHERE dan HAVING bener? (HAVING buat filter SETELAH GROUP BY)
```

---

> **Pesan terakhir:** SQL itu kayak main LEGO. Kamu tinggal nyusun blok-blok perintah. Awalnya memang kaku, makin sering kamu main, makin hafal bentuk dan cara nyambunginnya.
>
> **Practice makes perfect. Langsung coba aja!** 🚀
