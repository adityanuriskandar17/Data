<p align="center">
    <img src="./../images/sql-masterclas-banner.png" alt="sql-masterclass-banner">
</p>

[![forthebadge](./../images/badges/version-1.0.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/powered-by-coffee.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/ctrl-c-ctrl-v.svg)]()

# Langkah 5 - Mari Mulai Analisis Data!

[![forthebadge](./../images/badges/go-to-previous-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step4.md)
[![forthebadge](./../images/badges/go-to-next-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step6.md)

Sekarang setelah kita menjelajahi ketiga tabel kita - mari kita coba visualisasikan bagaimana masing-masing tabel terhubung satu sama lain menggunakan Entity Relationship Diagram atau disingkat ERD!

## Apa itu ERD?

ERD sangat berguna untuk memvisualisasikan hubungan antar kolom dalam tabel - terutama ketika menggabungkannya menggunakan tabel joins (sesuatu yang akan kita bahas dalam tutorial ini)

Di bawah ini Anda akan melihat ERD untuk studi kasus kita saat ini - hal yang paling penting adalah memperhatikan bagaimana semua kolom saling berhubungan satu sama lain.

![Crypto Case Study ERD](assets/crypto-erd.png)

# Analitik Realistis

Meskipun kita telah mengeksplorasi dataset kita dan mempelajari beberapa konsep SQL dasar yang diperlukan untuk analisis data - kita belum menggabungkan query SQL kita ke dalam satu proses analitis terfokus untuk memecahkan masalah yang lebih besar. Ini adalah kesempatan kita untuk mencobanya sekarang!

Katakanlah kita ingin menganalisis kinerja portofolio keseluruhan dan juga kinerja setiap anggota berdasarkan semua data yang kita miliki di 3 tabel kita.

## Analisis Rentang

Pertama - mari kita lihat rentang data apa yang kita miliki!

### Pertanyaan 1

> Apa tanggal transaksi paling awal dan paling terakhir untuk semua anggota?

<details><summary>Klik di sini untuk melihat solusinya!</summary><br>

```sql
SELECT
  MIN(txn_date) AS earliest_date,
  MAX(txn_date) AS latest_date
FROM trading.transactions;
```

</details><br>

| earliest_date | latest_date |
| ------------- | ----------- |
| 2017-01-01    | 2021-08-27  |

### Pertanyaan 2

> Apa rentang nilai `market_date` yang tersedia di data harga?

<details><summary>Klik di sini untuk melihat solusinya!</summary><br>

```sql
SELECT
  MIN(market_date) AS earliest_date,
  MAX(market_date) AS latest_date
FROM trading.prices;
```

</details><br>

| earliest_date | latest_date |
| ------------- | ----------- |
| 2017-01-01    | 2021-08-29  |
<br>

## Menggabungkan Dataset Kita

Sekarang setelah kita mengetahui rentang tanggal kita dari Januari 2017 hingga hampir akhir Agustus 2021 untuk dataset harga dan transaksi - kita dapat mulai menggabungkan kedua tabel ini!

Mari gunakan ERD yang ditunjukkan di atas untuk menggabungkan tabel `trading.transactions` dan tabel `trading.members` untuk menjawab beberapa pertanyaan sederhana tentang mentor kita!

### Pertanyaan 3

> 3 mentor teratas mana yang memiliki kuantitas Bitcoin paling banyak per tanggal 29 Agustus?

<details><summary>Klik di sini untuk melihat solusinya!</summary><br>

```sql
SELECT
  members.first_name,
  SUM(
    CASE
      WHEN transactions.txn_type = 'BUY'  THEN transactions.quantity
      WHEN transactions.txn_type = 'SELL' THEN -transactions.quantity
    END
  ) AS total_quantity
FROM trading.transactions
INNER JOIN trading.members
  ON transactions.member_id = members.member_id
WHERE ticker = 'BTC'
GROUP BY members.first_name
ORDER BY total_quantity DESC
LIMIT 3;
```

</details><br>

| first_name |     total_quantity      |
| ---------- | ----------------------- |
| Nandita    | 4160.219869506641749735 |
| Leah       |  4046.09089667256706404 |
| Ayush      |  3945.19808326050497234 |
<br>

## Menghitung Nilai Portofolio

Sekarang mari kita gabungkan semua 3 tabel bersama-sama hanya dengan `INNER JOIN` sehingga kita dapat memanfaatkan semua dataset kita secara bersamaan.

### Pertanyaan 4

> Berapa total nilai semua portofolio Ethereum untuk setiap region pada tanggal akhir analisis kita? Urutkan output berdasarkan nilai portofolio menurun

<details><summary>Klik di sini untuk melihat solusinya!</summary><br>

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
  ) * cte_latest_price.price AS ethereum_value,
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

</details><br>

|    region     |        ethereum_value        |    avg_ethereum_value     |
| ------------- | ---------------------------- | ------------------------- |
| Australia     | 40076021.0922707343527642712 | 10752.8900167080049298064 |
| United States | 50688412.2772532532882719016 | 10549.0972481276281626456 |
| Asia          |  5011670.9776990206825808176 |  8933.4598532959370421432 |
| India         |   6276426.482786365114210656 |   8036.397545181005116104 |
| Africa        |  2183933.3382704268238606128 |  3899.8809611971907658600 |
<br>

### Pertanyaan 5

> Berapa nilai rata-rata setiap portofolio Ethereum di setiap region? Urutkan output ini dalam urutan menurun

<details><summary>Klik di sini untuk melihat solusinya!</summary><br>

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

</details><br>

|    region     |    avg_ethereum_value     |
| ------------- | ------------------------- |
| Australia     | 10752.8900167080049298064 |
| United States | 10549.0972481276281626456 |
| Asia          |  8933.4598532959370421432 |
| India         |   8036.397545181005116104 |
| Africa        |  3899.8809611971907658600 |
<br>

Hmm tunggu sebentar...apakah output dari query di atas terlihat benar bagi Anda?

Mari kita coba lagi - kali ini kita akan menghitung total jumlah nilai portofolio dan kemudian membaginya secara manual dengan jumlah total mentor di setiap region!

<details><summary>Klik di sini untuk melihat solusinya!</summary><br>

```sql
WITH cte_latest_price AS (
  SELECT
    ticker,
    price
  FROM trading.prices
  WHERE ticker = 'ETH'
  AND market_date = '2021-08-29'
),
cte_calculations AS (
SELECT
  members.region,
  SUM(
    CASE
      WHEN transactions.txn_type = 'BUY'  THEN transactions.quantity
      WHEN transactions.txn_type = 'SELL' THEN -transactions.quantity
    END
  ) * cte_latest_price.price AS ethereum_value,
  COUNT(DISTINCT members.member_id) AS mentor_count
FROM trading.transactions
INNER JOIN cte_latest_price
  ON transactions.ticker = cte_latest_price.ticker
INNER JOIN trading.members
  ON transactions.member_id = members.member_id
WHERE transactions.ticker = 'ETH'
GROUP BY members.region, cte_latest_price.price
)
-- output akhir
SELECT
  *,
  ethereum_value / mentor_count AS avg_ethereum_value
FROM cte_calculations
ORDER BY avg_ethereum_value DESC;
```

</details><br>

|    region     |        ethereum_value        | mentor_count |      avg_ethereum_value      |
| ------------- | ---------------------------- | ------------ | ---------------------------- |
| Australia     | 40076021.0922707343527642712 |            4 | 10019005.2730676835881910678 |
| United States | 50688412.2772532532882719016 |            7 |  7241201.7538933218983245574 |
| India         |   6276426.482786365114210656 |            1 |   6276426.482786365114210656 |
| Asia          |  5011670.9776990206825808176 |            1 |  5011670.9776990206825808176 |
| Africa        |  2183933.3382704268238606128 |            1 |  2183933.3382704268238606128 |
<br>

[![forthebadge](./../images/badges/go-to-previous-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step4.md)
[![forthebadge](./../images/badges/go-to-next-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step6.md)
