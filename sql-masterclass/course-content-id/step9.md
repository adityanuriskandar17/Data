<p align="center">
    <img src="./../images/sql-masterclas-banner.png" alt="sql-masterclass-banner">
</p>

[![forthebadge](./../images/badges/version-1.0.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/powered-by-coffee.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/ctrl-c-ctrl-v.svg)]()

# Langkah 9 - Analisis Beli dan Tahan

[![forthebadge](./../images/badges/go-to-previous-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step8.md)
[![forthebadge](./../images/badges/go-to-next-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step10.md)

![hodl](assets/hodl.jpeg)

Kenali Leah - dia adalah mentor kami yang akan menerapkan strategi beli dan tahan atau yang dikenal sebagai "strategi HODL" atau hold on for dear life!

Dia menghindari risiko dan hanya ingin membiarkan investasi awalnya begitu saja karena dia percaya kepemilikan awalnya akan tumbuh seiring waktu dengan risiko rendah.

## Riwayat Transaksi Leah

1. Dia membeli 50 BTC dan 50 ETH pada 1 Januari 2017
2. Dia menahan seluruh portofolionya dan tidak menjual apa pun (HODL)
3. Dia juga tidak membeli jumlah tambahan dari salah satu kripto tersebut
4. Pada 29 Agustus 2021 (tanggal terakhir data harga kami) - kita dapat menilai kinerja individualnya

> Ingat bahwa kita sedang menyederhanakan masalah kita saat ini, sehingga catatan Leah sebenarnya akan berbeda dalam dataset `trading.transactions` yang asli!

## Data

Untuk skenario sederhana ini - pertama-tama kita perlu membuat tabel temp baru bernama `leah_hodl_strategy` menggunakan kode di bawah ini:

```sql
CREATE TEMP TABLE leah_hodl_strategy AS
SELECT * FROM trading.transactions
WHERE member_id = 'c20ad4'
AND txn_date = '2017-01-01'
AND quantity = 50;
```

Anda dapat memeriksa data dengan menjalankan query berikut setelah membuat tabel temp di atas:

```sql
SELECT * FROM leah_hodl_strategy;
```

| txn_id | member_id | ticker |  txn_date  | txn_type | quantity | percentage_fee |      txn_time       |
| ------ | --------- | ------ | ---------- | -------- | -------- | -------------- | ------------------- |
|     12 | c20ad4    | BTC    | 2017-01-01 | BUY      |       50 |           0.30 | 2017-01-01 00:00:00 |
|     26 | c20ad4    | ETH    | 2017-01-01 | BUY      |       50 |           0.30 | 2017-01-01 00:00:00 |
<br>

## Metrik yang Diperlukan

Untuk skenario dasar ini - kami ingin menghitung metrik berikut:

1. Nilai awal dari pembelian 50 BTC dan 50 ETH miliknya
2. Jumlah biaya dalam dolar yang dia bayarkan untuk 2 transaksi tersebut
3. Nilai akhir portofolionya pada 29 Agustus 2021
4. Profitabilitas dengan membagi nilai akhir dengan nilai awal

## Solusi

### Pertanyaan 1 & 2

Kita dapat menghitung 2 pertanyaan pertama menggunakan satu query

> 1. Nilai awal dari pembelian 50 BTC dan 50 ETH miliknya
> 2. Jumlah biaya dalam dolar yang dia bayarkan untuk 2 transaksi tersebut

<details><summary>Klik di sini untuk menampilkan solusi!</summary><br>

```sql
SELECT
  SUM(transactions.quantity * prices.price) AS initial_value,
  SUM(transactions.quantity * prices.price * transactions.percentage_fee / 100) AS fees
FROM leah_hodl_strategy AS transactions
INNER JOIN trading.prices
  ON transactions.ticker = prices.ticker
  AND transactions.txn_date = prices.market_date;
```

</details><br>

| initial_value |         fees         |
| ------------- | -------------------- |
|      50180.00 | 150.5400000000000000 |
<br>

### Pertanyaan 3

> Nilai akhir portofolionya pada 29 Agustus 2021

<details><summary>Klik di sini untuk menampilkan solusi!</summary><br>

```sql
SELECT
  SUM(transactions.quantity * prices.price) AS final_value
FROM leah_hodl_strategy AS transactions
INNER JOIN trading.prices
  ON transactions.ticker = prices.ticker
WHERE prices.market_date = '2021-08-29';
```

</details><br>

| final_value |
| ----------- |
|  2571642.00 |

### Pertanyaan 4

> Hitung profitabilitas dengan membagi nilai akhir Leah dengan nilai awal

Kita sebenarnya dapat melakukan yang lebih baik dan menggabungkan semua 4 metrik ke dalam satu query!

<details><summary>Klik di sini untuk menampilkan solusi!</summary><br>

```sql
WITH cte_portfolio_values AS (
  SELECT
    -- initial metrics
    SUM(transactions.quantity * initial.price) AS initial_value,
    SUM(transactions.quantity * initial.price * transactions.percentage_fee / 100) AS fees,
    -- final value
    SUM(transactions.quantity * final.price) AS final_value
  FROM leah_hodl_strategy AS transactions
  INNER JOIN trading.prices AS initial
    ON transactions.ticker = initial.ticker
    AND transactions.txn_date = initial.market_date
  INNER JOIN trading.prices AS final
    ON transactions.ticker = final.ticker
  WHERE final.market_date = '2021-08-29'
)
SELECT
  initial_value,
  fees,
  final_value,
  final_value / initial_value AS profitability
FROM cte_portfolio_values;
```

</details><br>

| initial_value |         fees         | final_value |    profitability    |
| ------------- | -------------------- | ----------- | ------------------- |
|      50180.00 | 150.5400000000000000 |  2571642.00 | 51.2483459545635711 |
<br>

[![forthebadge](./../images/badges/go-to-previous-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step8.md)
[![forthebadge](./../images/badges/go-to-next-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step10.md)
