# 🔍 Cara Membaca Query CTE + JOIN + Agregasi

## Query yang Dibahas

```sql
WITH cte_latest_price AS (
  SELECT
    ticker,
    price
  FROM trading.prices
  WHERE ticker = 'ETH'
    AND market_date = '2021-08-29'
)
SELECT
  members.region,
  SUM(
    CASE
      WHEN transactions.txn_type = 'BUY'  THEN transactions.quantity
      WHEN transactions.txn_type = 'SELL' THEN -transactions.quantity
    END
  ) * cte_latest_price.price AS total_ethereum_value,
  AVG(
    CASE
      WHEN transactions.txn_type = 'BUY'  THEN transactions.quantity
      WHEN transactions.txn_type = 'SELL' THEN -transactions.quantity
    END
  ) * cte_latest_price.price AS avg_ethereum_value
FROM trading.transactions
INNER JOIN cte_latest_price
  ON transactions.ticker = cte_latest_price.ticker
INNER JOIN trading.members
  ON transactions.member_id = members.member_id
WHERE transactions.ticker = 'ETH'
GROUP BY members.region, cte_latest_price.price
ORDER BY avg_ethereum_value DESC;
```

---

## 🧠 Cara Baca Step-by-Step

---

### 🔹 STEP 0: CTE — Bikin Tabel Sementara

```sql
WITH cte_latest_price AS (
  SELECT ticker, price
  FROM trading.prices
  WHERE ticker = 'ETH'
    AND market_date = '2021-08-29'
)
```

**Artinya:** Cari harga ETH pas tanggal 29 Agustus 2021.

Hasil CTE-nya cuma **1 baris**:

```
┌─────────────────────────────────────────────────────────────┐
│  cte_latest_price (tabel sementara)                         │
│  ┌────────┬──────────┐                                      │
│  │ ticker │ price    │                                      │
│  ├────────┼──────────┤                                      │
│  │ 'ETH'  │ 3177.84  │  ← harga ETH per 29 Agustus 2021     │
│  └────────┴──────────┘                                      │
└─────────────────────────────────────────────────────────────┘
```

---

### 🔹 STEP 1: FROM — Ambil Data

```sql
FROM trading.transactions
```

Semua data dari tabel `transactions`. Isinya ribuan baris — catatan beli & jual crypto.

---

### 🔹 STEP 2: INNER JOIN — Nyambungin ke Harga

```sql
INNER JOIN cte_latest_price
  ON transactions.ticker = cte_latest_price.ticker
```

#### 📌 INI YANG PALING MUNGKIN MEMBINGUNGKAN

**Apa yang terjadi?** Setiap baris di `transactions` dicocokin ke `cte_latest_price` lewat kolom `ticker`.

Tapi `cte_latest_price` cuma punya **1 baris** — yaitu ETH dengan harga 3177.84.

Jadi yang terjadi:

```
transactions (ribuan baris)
┌───────────┬────────┬──────────┬──────────┐
│ member_id │ ticker │ txn_type │ quantity │
├───────────┼────────┼──────────┼──────────┤
│ abc       │ ETH    │ BUY      │ 10       │──┐
│ def       │ ETH    │ SELL     │ 5        │──┤
│ abc       │ BTC    │ BUY      │ 2        │  │ ← ❌ BTC gak cocok, didrop!
│ def       │ ETH    │ BUY      │ 3        │──┤
└───────────┴────────┴──────────┴──────────┘  │
                                               │
    INNER JOIN ON ticker                        │
                                               │
┌─────────────────┐                            │
│ cte_latest_price│                            │
│ ┌──────┬──────┐ │                            │
│ │ ETH  │3177.8│ │◄───────────────────────────┘
│ └──────┴──────┘ │              (cocok: ETH = ETH)
└─────────────────┘

HASIL JOIN:
┌───────────┬────────┬──────────┬──────────┬────────┐
│ member_id │ ticker │ txn_type │ quantity │ price  │
├───────────┼────────┼──────────┼──────────┼────────┤
│ abc       │ ETH    │ BUY      │ 10       │ 3177.8 │
│ def       │ ETH    │ SELL     │ 5        │ 3177.8 │
│ def       │ ETH    │ BUY      │ 3        │ 3177.8 │
└───────────┴────────┴──────────┴──────────┴────────┘
```

> **Kenapa BTC ilang?** Karena INNER JOIN cuma ambil yang cocok. BTC gak cocok sama ETH di CTE, jadi baris BTC **dibuang**.

---

### 🔹 STEP 3: INNER JOIN — Nyambungin ke Members

```sql
INNER JOIN trading.members
  ON transactions.member_id = members.member_id
```

Setelah dapet harga, sekarang dicocokin lagi ke tabel `members` biar kita tahu **siapa punya nama dan region apa**.

```
SEBELUM JOIN MEMBERS:
┌───────────┬────────┬──────────┬──────────┬────────┐
│ member_id │ ticker │ txn_type │ quantity │ price  │
├───────────┼────────┼──────────┼──────────┼────────┤
│ abc       │ ETH    │ BUY      │ 10       │ 3177.8 │
│ def       │ ETH    │ SELL     │ 5        │ 3177.8 │
│ def       │ ETH    │ BUY      │ 3        │ 3177.8 │
└───────────┴────────┴──────────┴──────────┴────────┘

INNER JOIN members ON member_id

members:
┌───────────┬───────────┬──────────┐
│ member_id │ first_name│ region   │
├───────────┼───────────┼──────────┤
│ abc       │ Adi       │ Asia     │
│ def       │ Budi      │ US       │
└───────────┴───────────┴──────────┘

HASIL JOIN:
┌───────────┬──────────┬──────────┬──────────┬────────┬──────────┐
│ member_id │ txn_type │ quantity │ price    │ name   │ region   │
├───────────┼──────────┼──────────┼──────────┼────────┼──────────┤
│ abc       │ BUY      │ 10       │ 3177.8   │ Adi    │ Asia     │
│ def       │ SELL     │ 5        │ 3177.8   │ Budi   │ US       │
│ def       │ BUY      │ 3        │ 3177.8   │ Budi   │ US       │
└───────────┴──────────┴──────────┴──────────┴────────┴──────────┘
```

---

### 🔹 STEP 4: WHERE — Filter Lagi

```sql
WHERE transactions.ticker = 'ETH'
```

Sebenernya ini **udah gak terlalu berguna** karena JOIN tadi udah otomatis milah ETH doang. Tapi ini bentuknya jaga-jaga aja.

---

### 🔹 STEP 5: GROUP BY — Kelompokin per Region

```sql
GROUP BY members.region, cte_latest_price.price
```

Data dikelompokin **per region**. Kolom `price` diikutkan ke GROUP BY karena dipake di SELECT, tapi isinya sama semua (3177.84).

```
SEBELUM GROUP BY:
┌──────────┬──────────┬──────────┬────────┬──────────┐
│ region   │ txn_type │ quantity │ price  │ name     │
├──────────┼──────────┼──────────┼────────┼──────────┤
│ Asia     │ BUY      │ 10       │ 3177.8 │ Adi      │
│ US       │ SELL     │ 5        │ 3177.8 │ Budi     │
│ US       │ BUY      │ 3        │ 3177.8 │ Budi     │
└──────────┴──────────┴──────────┴────────┴──────────┘

GROUP BY region:
┌──────────┐
│ Asia     │ ─→ quantity: BUY 10 → net = +10
│          │
│ US       │ ─→ quantity: SELL 5 (-5) + BUY 3 (+3) → net = -2
└──────────┘
```

---

### 🔹 STEP 6: SUM & AVG — Hitung Value

```sql
SUM(
  CASE WHEN txn_type = 'BUY' THEN quantity
       WHEN txn_type = 'SELL' THEN -quantity
  END
) * cte_latest_price.price AS total_ethereum_value
```

#### 📌 Cara Baca CASE WHEN

```
CASE 
  WHEN txn_type = 'BUY'  THEN quantity    → kalau beli, quantity-nya POSITIF
  WHEN txn_type = 'SELL' THEN -quantity   → kalau jual, quantity-nya NEGATIF
END
```

**Logika:** Bayangin kamu punya kotak ETH.
- Setiap kali beli (BUY) → kamu **masukin** ETH [positif]
- Setiap kali jual (SELL) → kamu **ngeluarin** ETH [negatif]
- `SUM(...)` → hitung **sisa ETH di kotak**
- `SUM(...) * price` → kalikan dengan harga → **total nilai ETH-mu dalam rupiah/dollar**

#### 🎯 Analogi

Kamu jualan es teh:
```
Beli gelas  → masuk stok: +10 gelas
Jual 3 gelas → keluar stok: -3 gelas
Beli lagi 5  → masuk stok: +5 gelas
------------------------------
Sisa stok   = 10 - 3 + 5 = 12 gelas
Nilai stok  = 12 × Rp2.000 = Rp24.000
```

Nah itu persis yang dilakukan query ini — bedanya dihitung per region.

---

### 🔹 STEP 7: Hasil Akhir

```
REGION: ASIA
  BUY  10 ETH  (+10)
  -----------------
  Net:  10 ETH
  Nilai: 10 × 3177.84 = 31.778,4

REGION: US
  SELL 5 ETH  (-5)
  BUY  3 ETH  (+3)
  -----------------
  Net:  -2 ETH
  Nilai: -2 × 3177.84 = -6.355,68
```

Hasil akhir query:

| region | total_ethereum_value | avg_ethereum_value |
|--------|--------------------|--------------------|
| Asia | 31,778.4 | 31,778.4 |
| US | -6,355.68 | -6,355.68 |

---

## 📊 Flow Diagram Lengkap

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  CTE: cte_latest_price                                          │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Cari harga ETH per 29 Agustus → (ETH, 3177.84)           │  │
│  └──────────────────────────┬────────────────────────────────┘  │
│                             │                                    │
│                             ▼                                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ FROM transactions                                         │  │
│  │   │                                                       │  │
│  │   ▼                                                       │  │
│  │ INNER JOIN cte_latest_price ON ticker                     │  │
│  │   │ → ambil yg ETH doang, kasi harga 3177.84             │  │
│  │   ▼                                                       │  │
│  │ INNER JOIN members ON member_id                           │  │
│  │   │ → sambungin ke data member (nama, region)             │  │
│  │   ▼                                                       │  │
│  │ WHERE ticker = 'ETH' (udah otomatis, jaga-jaga)           │  │
│  │   │                                                       │  │
│  │   ▼                                                       │  │
│  │ GROUP BY region                                           │  │
│  │   │ → kelompokin per region                               │  │
│  │   │ → SUM(...) → net ETH per region                      │  │
│  │   │ → SUM(...) × price → total nilai ETH per region      │  │
│  │   │ → AVG(...) × price → rata-rata nilai ETH             │  │
│  │   ▼                                                       │  │
│  │ ORDER BY avg_ethereum_value DESC                          │  │
│  │   │ → urutin dari nilai rata-rata tertinggi               │  │
│  └───────────────────────────────────────────────────────────┘  │
│                             │                                    │
│                             ▼                                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ HASIL: Nilai total ETH yang dimiliki setiap region        │  │
│  │        (diukur dengan harga 29 Agustus 2021)              │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Fokus: INNER JOIN

### INNER JOIN Itu Sebenarnya Apa?

**INNER JOIN** = **AMBIL YANG COCOK DOANG**

```
TABEL A                                  TABEL B
┌──────┐        INNER JOIN              ┌──────┐
│  A   │    ───────────────────────→     │  B   │
│ ───  │    HANYA baris yang ADA        │ ───  │
│  1   │    di KEDUA tabel               │  1   │
│  2   │                                 │  3   │
│  3   │                                 │  4   │
└──────┘                                 └──────┘

HASIL INNER JOIN:
┌──────┬──────┐
│ A.1  │ B.1  │  ← cocok
│ A.3  │ B.3  │  ← cocok
└──────┴──────┘

A.2 → ❌ gak ada di tabel B, dibuang
B.4 → ❌ gak ada di tabel A, dibuang
```

### 🎯 Analogi INNER JOIN

Kamu punya **2 daftar**:

**Daftar 1 — Siswa:**
| No | Nama |
|----|------|
| 1 | Adi |
| 2 | Budi |
| 3 | Caca |

**Daftar 2 — Nilai Ujian:**
| No | Nilai |
|----|-------|
| 1 | 90 |
| 3 | 85 |
| 4 | 70 |

`INNER JOIN ON No` → ambil yang nomornya cocok:

| Nama | Nilai |
|------|-------|
| Adi | 90 | ← No 1 cocok
| Caca | 85 | ← No 3 cocok

Budi ❌ (gak ada nilai) — diabaikan
No 4 ❌ (gak ada siswanya) — diabaikan

### 🔑 Inti INNER JOIN di Query Ini

```
transactions                                            members
┌───────────┬────────┐       INNER JOIN ON member_id    ┌───────────┬──────────┐
│ member_id │ ticker │       ──────────────────────→    │ member_id │ region   │
├───────────┼────────┤                                  ├───────────┼──────────┤
│ C4CA42    │ ETH    │  ── cocok ──→                   │ C4CA42    │ Australia│
│ C81E72    │ ETH    │  ── cocok ──→                   │ C81E72    │ US       │
│ XXXXXX    │ ETH    │  ── ❌ gak ada di members →     │           │          │
└───────────┴────────┘                                  └───────────┴──────────┘
```

- Kalau ada transaksi dari `member_id` yang **gak terdaftar** di `members` → transaksi itu **dibuang**
- Kalau ada member yang **gak pernah transaksi** → member itu **gak muncul**

---

## 💡 Ringkasan

Query ini jawab pertanyaan:

> **"Berapa total nilai ETH yang dimiliki setiap region berdasarkan harga 29 Agustus 2021?"**

### Cara kerjanya:
1. Ambil harga ETH per 29 Agustus (`cte_latest_price`)
2. JOIN ke transaksi → cuma ambil transaksi ETH (`INNER JOIN`)
3. JOIN ke members → dapet region (`INNER JOIN`)
4. Kelompokin per region (`GROUP BY`)
5. Hitung net ETH (BUY = +, SELL = -) lalu kalikan harga (`SUM(CASE...) * price`)
6. Urutin dari nilai terbanyak

### ⚠️ Catatan:
- `AVG(...) * price` di query ini hasilnya **sama dengan** `SUM(...) * price` karena per region cuma ada 1 nilai rata-rata (AVG dari 1 baris = nilai itu sendiri)
- Sebenarnya fungsi `AVG` di sini kurang masuk akal — lebih tepat pake `SUM` aja

---

## 📝 Latihan

Coba modifikasi sendiri untuk paham JOIN:

```sql
-- 1. Ganti INNER JOIN → LEFT JOIN, lihat bedanya
SELECT m.first_name, COUNT(t.txn_id)
FROM trading.members m
LEFT JOIN trading.transactions t ON m.member_id = t.member_id
GROUP BY m.first_name;
-- → semua member muncul, yang gak transaksi dapet 0
```

```sql
-- 2. Ganti INNER JOIN → RIGHT JOIN
SELECT m.first_name, COUNT(t.txn_id)
FROM trading.members m
RIGHT JOIN trading.transactions t ON m.member_id = t.member_id
GROUP BY m.first_name;
-- → cuma member yang pernah transaksi aja
```

```bash
# Jalanin di psql
psql -d sql_masterclass
```
