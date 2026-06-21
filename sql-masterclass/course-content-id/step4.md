<p align="center">
    <img src="./../images/sql-masterclas-banner.png" alt="sql-masterclass-banner">
</p>

[![forthebadge](./../images/badges/version-1.0.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/powered-by-coffee.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/ctrl-c-ctrl-v.svg)]()

# Langkah 4 - Tabel Transaksi

[![forthebadge](./../images/badges/go-to-previous-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step3.md)
[![forthebadge](./../images/badges/go-to-next-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step5.md)

Di tabel database `trading.transactions` ketiga kita, terdapat setiap transaksi `BUY` atau `SELL` untuk `ticker` tertentu yang dilakukan oleh setiap `member`

## Lihat Data

Anda dapat memeriksa 10 transaksi terbaru berdasarkan `member_id = 'c4ca42'` (apakah Anda ingat siapa itu?)

```sql
SELECT * FROM trading.transactions
WHERE member_id = 'c4ca42'
ORDER BY txn_time DESC
LIMIT 10;
```

## Kamus Data

| Nama Kolom     | Deskripsi                        |
| -------------- | --------------------------------- |
| txn_id         | ID unik untuk setiap transaksi    |
| member_id      | pengenal anggota untuk setiap perdagangan |
| ticker         | ticker untuk setiap perdagangan   |
| txn_date       | tanggal untuk setiap transaksi    |
| txn_type       | BUY atau SELL                     |
| quantity       | total kuantitas untuk setiap perdagangan |
| percentage_fee | % dari jumlah total yang dibebankan sebagai biaya |
| txn_time       | timestamp untuk setiap perdagangan |
<br>

## Pertanyaan Transaksi

Mari kita selesaikan eksplorasi data awal kita dengan beberapa pertanyaan lagi untuk tabel `trading.transactions`!

### Pertanyaan 1

> Berapa banyak record yang ada di tabel `trading.transactions`?

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>
<br>

```sql
SELECT COUNT(*) FROM trading.transactions;
```

</details>
<br>

### Pertanyaan 2

> Berapa banyak transaksi unik yang ada?

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>
<br>

```sql
SELECT COUNT(DISTINCT txn_id) FROM trading.transactions;
```

</details>
<br>

| count |
| ----- |
| 22918 |
<br>

### Pertanyaan 3

> Berapa banyak transaksi beli dan jual untuk Bitcoin?

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>
<br>

```sql
SELECT
  txn_type,
  COUNT(*) AS transaction_count
FROM trading.transactions
WHERE ticker = 'BTC'
GROUP BY txn_type;
```

</details>
<br>

| txn_type | transaction_count |
| -------- | ----------------- |
| SELL     |              2044 |
| BUY      |             10440 |
<br>

### Pertanyaan 4

> Untuk setiap tahun, hitung metrik beli dan jual berikut untuk Bitcoin:

* total jumlah transaksi
* total kuantitas
* rata-rata kuantitas per transaksi

Juga bulatkan kolom kuantitas ke 2 angka desimal.

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>
<br>

```sql
SELECT
  EXTRACT(YEAR FROM txn_date) AS txn_year,
  txn_type,
  COUNT(*) AS transaction_count,
  ROUND(SUM(quantity)::NUMERIC, 2) AS total_quantity,
  ROUND(AVG(quantity)::NUMERIC, 2) AS average_quantity
FROM trading.transactions
WHERE ticker = 'BTC'
GROUP BY txn_year, txn_type
ORDER BY txn_year, txn_type;
```

</details>
<br>

| txn_year | txn_type | transaction_count | total_quantity | average_quantity |
| -------- | -------- | ----------------- | -------------- | ---------------- |
|     2017 | BUY      |              2261 |       12069.58 |             5.34 |
|     2017 | SELL     |               419 |        2160.22 |             5.16 |
|     2018 | BUY      |              2204 |       11156.06 |             5.06 |
|     2018 | SELL     |               433 |        2145.05 |             4.95 |
|     2019 | BUY      |              2192 |       11114.43 |             5.07 |
|     2019 | SELL     |               443 |        2316.24 |             5.23 |
|     2020 | BUY      |              2350 |       11748.76 |             5.00 |
|     2020 | SELL     |               456 |        2301.98 |             5.05 |
|     2021 | BUY      |              1433 |        7161.32 |             5.00 |
|     2021 | SELL     |               293 |        1478.00 |             5.04 |
<br>

### Pertanyaan 5

> Berapa total kuantitas bulanan yang dibeli dan dijual untuk Ethereum di tahun 2020?

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>
<br>

```sql
SELECT
  DATE_TRUNC('MON', txn_date)::DATE AS calendar_month,
  SUM(CASE WHEN txn_type = 'BUY' THEN quantity ELSE 0 END) AS buy_quantity,
  SUM(CASE WHEN txn_type = 'SELL' THEN quantity ELSE 0 END) AS sell_quantity
FROM trading.transactions
WHERE txn_date BETWEEN '2020-01-01' AND '2020-12-31'
  AND ticker = 'ETH'
GROUP BY calendar_month
ORDER BY calendar_month;
```

</details>
<br>

| calendar_month |   buy_quantity    |   sell_quantity    |    
| -------------- | ----------------- | ------------------ |
| 2020-01-01     | 801.0541163041565 |  158.1272716986775 |
| 2020-02-01     | 687.8912804600265 | 160.06533517839912 |
| 2020-03-01     | 804.2368342042604 |  182.1895644691428 |
| 2020-04-01     |   761.87446914631 | 203.16695745059786 |
| 2020-05-01     | 787.4238801914097 | 149.08328330131854 |
| 2020-06-01     | 787.4659503521506 |  208.3362898912813 |
| 2020-07-01     | 890.7807530272569 | 117.01628097387932 |
| 2020-08-01     | 800.6004484214079 |  178.5423079909115 |
| 2020-09-01     |  767.654783160818 | 118.86826373014458 |
| 2020-10-01     | 744.7913667867248 |   174.269279883162 |
| 2020-11-01     | 698.0915637008526 | 163.74629299419385 |
| 2020-12-01     | 752.4121935735661 | 212.77643601396653 |
<br>

### Pertanyaan 6

> Ringkas semua transaksi beli dan jual untuk setiap `member_id` dengan menghasilkan 1 baris untuk setiap anggota dengan kolom tambahan berikut:

* Kuantitas beli Bitcoin
* Kuantitas jual Bitcoin
* Kuantitas beli Ethereum
* Kuantitas jual Ethereum

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>
<br>

```sql
SELECT
  member_id,
  SUM(
    CASE
      WHEN ticker = 'BTC' AND txn_type = 'BUY' THEN quantity
      ELSE 0
    END
  ) AS btc_buy_qty,
  SUM(
    CASE
      WHEN ticker = 'BTC' AND txn_type = 'SELL' THEN quantity
      ELSE 0
    END
  ) AS btc_sell_qty,
  SUM(
    CASE
      WHEN ticker = 'ETH' AND txn_type = 'BUY' THEN quantity
      ELSE 0
    END
  ) AS eth_buy_qty,
  SUM(
    CASE
      WHEN ticker = 'BTC' AND txn_type = 'SELL' THEN quantity
      ELSE 0
    END
  ) AS eth_sell_qty
FROM trading.transactions
GROUP BY member_id;
```

</details>
<br>

| member_id |       btc_buy_qty       |     btc_sell_qty      |      eth_buy_qty       |     eth_sell_qty      |
| --------- | ----------------------- | --------------------- | ---------------------- | --------------------- |
| d3d944    |   4270.8573823425313401 | 735.87222217343213249 | 1744.65425673609669642 | 735.87222217343213249 |
| c20ad4    |  4975.75064119164404784 |  929.6597445190769838 |  2187.1154401373141792 |  929.6597445190769838 |
| c9f0f8    |   4572.8800842388871361 |  852.3638794847991004 |  2343.4690790139731866 |  852.3638794847991004 |
| eccbc8    |  2844.65155099725936589 |   305.345489355233177 |   2573.754757641582429 |   305.345489355233177 |
| 167909    |  4448.23880624893711454 |  503.0407229884321422 |  1119.7353314008790779 |  503.0407229884321422 |
| c81e72    |   2600.9308762349498788 | 974.09502352354264169 | 4852.52157101720575379 | 974.09502352354264169 |
| e4da3b    |   3567.3882471515063849 | 998.37853535959315513 |  2053.9833252960165058 | 998.37853535959315513 |
| c51ce4    |   2580.4064599247725600 | 1028.7200828179673870 |  2394.7300314796354124 | 1028.7200828179673870 |
| a87ff6    | 5023.705687783492459935 |  863.4858182768507102 |  3822.0371970017654265 |  863.4858182768507102 |
| 8f14e4    |   2647.0768334782105019 |   445.743862547520261 | 3233.47685039578173973 |   445.743862547520261 |
| 45c48c    |   3814.2424689381731354 |   198.131022250011036 | 4442.13685422790551869 |   198.131022250011036 |
| c4ca42    |   4380.4429315724604872 | 1075.5626055691556454 |  4516.5972484100717280 | 1075.5626055691556454 |
| 6512bd    |   4031.6925788360780822 | 574.78279876648434158 |  2941.2223099752008596 | 574.78279876648434158 |
| aab323    |   3491.8873912094965336 |  916.3032786678013621 | 4373.76210149024236043 |  916.3032786678013621 |
<br>

### Pertanyaan 7

> Berapa kuantitas akhir kepemilikan Bitcoin untuk setiap anggota? Urutkan output dari kepemilikan BTC tertinggi ke terendah

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>
<br>

```sql
SELECT
  member_id,
  SUM(
    CASE
      WHEN txn_type = 'BUY' THEN quantity
      WHEN txn_type = 'SELL' THEN -quantity
      ELSE 0
    END
  ) AS final_btc_holding
FROM trading.transactions
WHERE ticker = 'BTC'
GROUP BY member_id
ORDER BY final_btc_holding DESC;
```

</details>
<br>

| member_id |    final_btc_holding    |
| --------- | ----------------------- |
| a87ff6    | 4160.219869506641749735 |
| c20ad4    |  4046.09089667256706404 |
| 167909    |  3945.19808326050497234 |
| c9f0f8    |   3720.5162047540880357 |
| 45c48c    |   3616.1114466881620994 |
| d3d944    |  3534.98516016909920761 |
| 6512bd    |  3456.90978006959374062 |
| c4ca42    |   3304.8803260033048418 |
| aab323    |   2575.5841125416951715 |
| e4da3b    |  2569.00971179191322977 |
| eccbc8    |  2539.30606164202618889 |
| 8f14e4    |   2201.3329709306902409 |
| c81e72    |  1626.83585271140723711 |
| c51ce4    |   1551.6863771068051730 |
<br>

### Pertanyaan 8

> Anggota mana yang telah menjual kurang dari 500 Bitcoin? Urutkan output dari penjualan BTC terbanyak ke paling sedikit

Sebenarnya kita bisa melakukannya dengan 3 cara berbeda!

<details>
  <summary>Klik di sini untuk melihat solusi `HAVING`!</summary>
<br>

```sql
SELECT
  member_id,
  SUM(quantity) AS btc_sold_quantity
FROM trading.transactions
WHERE ticker = 'BTC'
  AND txn_type = 'SELL'
GROUP BY member_id
HAVING SUM(quantity) < 500
ORDER BY btc_sold_quantity DESC;
```

</details>
<br>

<details>
  <summary>Klik di sini untuk melihat solusi `CTE`!</summary>
<br>

```sql
WITH cte AS (
SELECT
  member_id,
  SUM(quantity) AS btc_sold_quantity
FROM trading.transactions
WHERE ticker = 'BTC'
  AND txn_type = 'SELL'
GROUP BY member_id
)
SELECT * FROM cte
WHERE btc_sold_quantity < 500
ORDER BY btc_sold_quantity DESC;
```

</details>
<br>

<details>
  <summary>Klik di sini untuk melihat solusi `subquery`!</summary>
<br>

```sql
SELECT * FROM (
  SELECT
    member_id,
    SUM(quantity) AS btc_sold_quantity
  FROM trading.transactions
  WHERE ticker = 'BTC'
    AND txn_type = 'SELL'
  GROUP BY member_id
) AS subquery
WHERE btc_sold_quantity < 500
ORDER BY btc_sold_quantity DESC;
```

</details>
<br>

| member_id |  btc_sold_quantity  |
| --------- | ------------------- |
| 8f14e4    | 445.743862547520261 |
| eccbc8    | 305.345489355233177 |
| 45c48c    | 198.131022250011036 |
<br>

### Pertanyaan 9

> Berapa total kuantitas Bitcoin yang dimiliki setiap `member_id` setelah menjumlahkan semua transaksi BUY dan SELL dari tabel `transactions`? Urutkan output berdasarkan total kuantitas menurun

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>
<br>

```sql
SELECT
  member_id,
  SUM(
    CASE
      WHEN txn_type = 'BUY'  THEN quantity
      WHEN txn_type = 'SELL' THEN -quantity
    END
  ) AS total_quantity
FROM trading.transactions
WHERE ticker = 'BTC'
GROUP BY member_id
ORDER BY total_quantity DESC;
```

</details>
<br>

| member_id |     total_quantity      |
| --------- | ----------------------- |
| a87ff6    | 4160.219869506641749735 |
| c20ad4    |  4046.09089667256706404 |
| 167909    |  3945.19808326050497234 |
| c9f0f8    |   3720.5162047540880357 |
| 45c48c    |   3616.1114466881620994 |
| d3d944    |  3534.98516016909920761 |
| 6512bd    |  3456.90978006959374062 |
| c4ca42    |   3304.8803260033048418 |
| aab323    |   2575.5841125416951715 |
| e4da3b    |  2569.00971179191322977 |
| eccbc8    |  2539.30606164202618889 |
| 8f14e4    |   2201.3329709306902409 |
| c81e72    |  1626.83585271140723711 |
| c51ce4    |   1551.6863771068051730 |
<br>

### Pertanyaan 10

> `member_id` mana yang memiliki rasio beli terhadap jual tertinggi berdasarkan kuantitas?

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>
<br>

```sql
SELECT
  member_id,
  SUM(CASE WHEN txn_type = 'BUY' THEN quantity ELSE 0 END) /
    SUM(CASE WHEN txn_type = 'SELL' THEN quantity ELSE 0 END) AS buy_to_sell_ratio
FROM trading.transactions
GROUP BY member_id
ORDER BY buy_to_sell_ratio DESC;
```

</details>
<br>

| member_id |  buy_to_sell_ratio   |
| --------- | -------------------- |
| 45c48c    | 19.91269871111331881 |
| a87ff6    | 7.486010484765204502 |
| c9f0f8    |   6.2499141870956191 |
| 8f14e4    |  5.30005322455443465 |
| eccbc8    |  4.92850232946761881 |
| c20ad4    |  4.65209743522270350 |
| 167909    |  4.60147388258864127 |
| aab323    |  4.55272149176427243 |
| 6512bd    |  4.52509140656952666 |
| c81e72    |  4.37533523692905634 |
| c4ca42    |   4.2628218979753569 |
| e4da3b    |  3.55762611425005570 |
| d3d944    |  3.35445896964968774 |
| c51ce4    |   2.3630130420937542 |
<br>

### Pertanyaan 11

> Untuk setiap `member_id` - bulan mana yang memiliki total kuantitas Ethereum terjual tertinggi?

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>
<br>

```sql
WITH cte_ranked AS (
SELECT
  member_id,
  DATE_TRUNC('MON', txn_date)::DATE AS calendar_month,
  SUM(quantity) AS sold_eth_quantity,
  RANK() OVER (PARTITION BY member_id ORDER BY SUM(quantity) DESC) AS month_rank
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

</details>
<br>

| member_id | calendar_month |  sold_eth_quantity  |
| --------- | -------------- | ------------------- |
| c51ce4    | 2017-05-01     |  66.092440429535028 |
| d3d944    | 2020-04-01     |  60.417369973983352 |
| 6512bd    | 2018-05-01     |   47.93285714951591 |
| 167909    | 2020-12-01     |   45.92423664055218 |
| c81e72    | 2018-08-01     |   41.26728177476413 |
| aab323    | 2018-09-01     | 41.1750763370983665 |
| c4ca42    | 2021-04-01     |  40.113474724022574 |
| c20ad4    | 2017-12-01     |   37.71908498970638 |
| eccbc8    | 2021-03-01     |  36.485934922948275 |
| 8f14e4    | 2017-07-01     |   36.17383743681231 |
| e4da3b    | 2019-01-01     |   30.48442641077632 |
| a87ff6    | 2020-07-01     |   27.28919836842423 |
| 45c48c    | 2020-01-01     |   20.21523406425370 |
| c9f0f8    | 2020-11-01     |  15.931855129247867 |

[![forthebadge](./../images/badges/go-to-previous-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step3.md)
[![forthebadge](./../images/badges/go-to-next-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step5.md)
