# 🔍 Cara Membaca Query CTE + RANK()

## Query yang Dibahas

```sql
WITH cte_ranked AS (
  SELECT
    member_id,
    DATE_TRUNC('MON', txn_date)::DATE AS calendar_month,
    SUM(quantity) AS sold_eth_quantity,
    RANK() OVER (
      PARTITION BY member_id
      ORDER BY SUM(quantity) DESC
    ) AS month_rank
  FROM trading.transactions
  WHERE ticker = 'ETH' AND txn_type = 'SELL'
  GROUP BY member_id, calendar_month
)
SELECT
  member_id,
  calendar_month,
  sold_eth_quantity
FROM cte_ranked
WHERE month_rank = 1
ORDER BY sold_eth_quantity DESC;
```

---

## 🧠 Cara Membaca: Kerjain dari DALEM ke LUAR

SQL itu dieksekusi **dari dalam ke luar**. Jadi kita baca dari bagian yang paling dalem dulu.

---

### 🔹 Layer 1: Ambil Data Mentah

```sql
FROM trading.transactions
WHERE ticker = 'ETH' AND txn_type = 'SELL'
```

**Artinya:** Ambil dari tabel `transactions`, **cuma yang jual ETH aja** (bukan BTC, bukan beli).

```
📦 SEMUA TRANSAKSI:
┌───────────┬────────┬──────────┬────────┐
│ member_id │ ticker │ txn_type │ jumlah │
├───────────┼────────┼──────────┼────────┤
│ abc       │ BTC    │ BUY      │ 10     │  ← ❌ diskip (bukan ETH)
│ abc       │ ETH    │ SELL     │ 5      │  ← ✅ dipake
│ def       │ ETH    │ SELL     │ 3      │  ← ✅ dipake
│ abc       │ ETH    │ BUY      │ 2      │  ← ❌ diskip (bukan SELL)
│ def       │ ETH    │ SELL     │ 7      │  ← ✅ dipake
└───────────┴────────┴──────────┴────────┘
```

---

### 🔹 Layer 2: Hitung per Kelompok (GROUP BY)

```sql
GROUP BY member_id, calendar_month
```

Di sini `calendar_month` itu hasil dari:

```sql
DATE_TRUNC('MON', txn_date)::DATE AS calendar_month
```

#### 📌 Cara Kerja DATE_TRUNC

`DATE_TRUNC('MON', tgl)` = **potong tanggalnya jadi awal bulan**. Kayak gunting — ambil bulan doang, harinya diganti 1.

```
Contoh:
'2021-06-15' → '2021-06-01'
'2021-06-28' → '2021-06-01'
'2021-07-03' → '2021-07-01'
'2021-07-25' → '2021-07-01'
```

Jadi semua transaksi di bulan yang sama dianggap satu kelompok.

#### 📌 Hasil GROUP BY

```
📊 DATA SETELAH DIKELOMPOKIN:
┌───────────┬────────────────┬──────────────────────┐
│ member_id │ calendar_month │ sold_eth_quantity    │
├───────────┼────────────────┼──────────────────────┤
│ abc       │ 2021-06-01     │ 5                    │  ← total jual Juni
│ abc       │ 2021-07-01     │ 8                    │  ← total jual Juli
│ def       │ 2021-06-01     │ 3                    │  ← total jual Juni
│ def       │ 2021-07-01     │ 7                    │  ← total jual Juli
│ def       │ 2021-08-01     │ 4                    │  ← total jual Agustus
└───────────┴────────────────┴──────────────────────┘
```

---

### 🔹 Layer 3: Kasih Ranking per Member

```sql
RANK() OVER (
  PARTITION BY member_id
  ORDER BY SUM(quantity) DESC
) AS month_rank
```

#### 📌 Cara Baca

| Keyword | Arti |
|---------|------|
| `RANK()` | Kasih nomor urut / peringkat |
| `OVER (...)` | Aturan cara ngasih peringkatnya |
| `PARTITION BY member_id` | **Direset per member**. Si abc punya ranking sendiri, si def punya sendiri |
| `ORDER BY SUM(quantity) DESC` | Ranking 1 = **paling banyak jualnya** |

#### 🎯 Analogi

Kayak lomba lari:
- `PARTITION BY member_id` = ganti peserta — setiap peserta mulai dari awal lagi
- `ORDER BY DESC` = liat siapa yang lari paling jauh — yang paling jauh dapet ranking 1
- `RANK()` = kasih medali emas (1), perak (2), perunggu (3)

```
┌───────────┬────────────────┬────────────────┬──────┐
│ member_id │ calendar_month │ sold_eth_qty   │ rank│
├───────────┼────────────────┼────────────────┼──────┤
│ abc       │ 2021-07-01     │ 8              │  1  │ ← juara
│ abc       │ 2021-06-01     │ 5              │  2  │
├───────────┼────────────────┼────────────────┼──────┤
│ def       │ 2021-07-01     │ 7              │  1  │ ← juara
│ def       │ 2021-08-01     │ 4              │  2  │
│ def       │ 2021-06-01     │ 3              │  3  │
└───────────┴────────────────┴────────────────┴──────┘
```

---

### 🔹 Layer 4: Ambil Ranking 1 Aja

```sql
WHERE month_rank = 1
```

CTE `cte_ranked` sudah jadi tabel sementara. Tinggal ambil yang **ranking 1** — artinya **bulan dengan penjualan terbanyak untuk setiap member**.

```
┌───────────┬────────────────┬────────────────┐
│ member_id │ calendar_month │ sold_eth_qty   │
├───────────┼────────────────┼────────────────┤
│ abc       │ 2021-07-01     │ 8              │  ← bulan terlaris abc
│ def       │ 2021-07-01     │ 7              │  ← bulan terlaris def
└───────────┴────────────────┴────────────────┘
```

Lalu `ORDER BY sold_eth_quantity DESC` = **urutin dari yang paling banyak jualnya**.

---

## 🎯 Analogi Dunia Nyata

Bayangin kamu punya catatan jualan semua pedagang di pasar:

```
1. 📋 Ambil semua nota → tapi cuma yang jualan ETH (bukan jualan saham/kambing)
2. 📆 Kelompokin per penjual per bulan → si abc jual berapa di Juni? Juli?
3. 🏆 Kasih ranking per penjual:
     - abc: Juli ranking 1 (jual 8), Juni ranking 2 (jual 5)
     - def: Juli ranking 1 (jual 7), Agustus ranking 2 (jual 4), Juni ranking 3 (jual 3)
4. 🎯 Tampilin yang ranking 1 aja → bulan terlaris tiap penjual
5. 📊 Urutin dari penjualan terbanyak ke paling sedikit
```

---

## 📊 Flow Diagram Lengkap

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  STEP 1: SEMUA DATA                                        │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ trading.transactions                                 │   │
│  │ ┌──────┬────────┬──────────┬─────────┬──────┐      │   │
│  │ │ id   │ ticker │ txn_type │ quantity │ tgl  │      │   │
│  │ ├──────┼────────┼──────────┼─────────┼──────┤      │   │
│  │ │ ...  │ BTC    │ BUY      │ ...     │ ...  │      │   │
│  │ │ ...  │ ETH    │ SELL     │ 5       │ ...  │      │   │
│  │ │ ...  │ ETH    │ SELL     │ 8       │ ...  │      │   │
│  │ └──────┴────────┴──────────┴─────────┴──────┘      │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                         ▼                                  │
│  STEP 2: FILTER                                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ WHERE ticker='ETH' AND txn_type='SELL'              │   │
│  │ → buang yang bukan ETH/BUY                          │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                         ▼                                  │
│  STEP 3: GROUP BY                                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ GROUP BY member_id, DATE_TRUNC('MON', txn_date)    │   │
│  │ → kelompokin per member per bulan                   │   │
│  │ → SUM(quantity) → total jual per bulan              │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                         ▼                                  │
│  STEP 4: RANK                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ RANK() OVER (                                       │   │
│  │   PARTITION BY member_id                            │   │
│  │   ORDER BY SUM(quantity) DESC                       │   │
│  │ )                                                   │   │
│  │ → ranking 1 = bulan paling laris per member         │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                         ▼                                  │
│  STEP 5: FILTER RANKING 1                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ WHERE month_rank = 1                                │   │
│  │ → ambil cuma yang ranking 1 (paling laris)          │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                         ▼                                  │
│  STEP 6: URUTKAN                                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ORDER BY sold_eth_quantity DESC                     │   │
│  │ → urutin dari yang paling banyak jualnya            │   │
│  └─────────────────────────────────────────────────────┘   │
│                         ▼                                  │
│  HASIL AKHIR:                                              │
│  ┌───────────┬────────────────┬────────────────┐           │
│  │ member_id │ calendar_month │ sold_eth_qty   │           │
│  ├───────────┼────────────────┼────────────────┤           │
│  │ abc       │ 2021-07-01     │ 8              │           │
│  │ def       │ 2021-07-01     │ 7              │           │
│  └───────────┴────────────────┴────────────────┘           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 💡 Intisari

### Query ini jawab pertanyaan:

> **"Kapan setiap member paling banyak jual ETH-nya? Dan siapa yang paling banyak?"**

### Output:
Tiap member muncul **cuma 1 baris** — yaitu **bulan terlarisnya** — diurut dari penjualan terbanyak.

### Kenapa pake CTE + RANK?
| Kenapa | Daripada |
|--------|----------|
| CTE bikin kode rapi, gak nested | Subquery yang bertumpuk |
| RANK() bisa kasih peringkat per grup | Harus bikin subquery manual buat ranking |
| PARTITION BY nge-reset per member | GROUP BY bakal ngeruntuhin data |

---

## 📝 Latihan: Coba Modifikasi Sendiri

```sql
-- 1. Ganti SELL → BUY (bulan paling banyak beli)
-- 2. Ganti ETH → BTC
-- 3. Ganti RANK → ROW_NUMBER (bedanya apa?)
-- 4. Ganti ORDER BY sold_eth_quantity DESC → ASC
-- 5. Tambahin LIMIT 3 (top 3 penjual terbanyak)
```

Coba modifikasi sendiri di psql:
```bash
psql -d sql_masterclass
```

Lalu paste query di atas dan ubah-ubah sendiri.
