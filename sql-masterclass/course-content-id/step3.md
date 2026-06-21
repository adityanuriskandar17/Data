<p align="center">
    <img src="./../images/sql-masterclas-banner.png" alt="sql-masterclass-banner">
</p>

[![forthebadge](./../images/badges/version-1.0.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/powered-by-coffee.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/ctrl-c-ctrl-v.svg)]()

# Langkah 3 - Harga Harian

[![forthebadge](./../images/badges/go-to-previous-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step2.md)
[![forthebadge](./../images/badges/go-to-next-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step4.md)

Kumpulan data berikutnya yang akan kita jelajahi adalah tabel `trading.prices` yang berisi data harga harian dan volume untuk 2 ticker cryptocurrency: `ETH` dan `BTC` (Ethereum dan Bitcoin!)

## Lihat Data

Sebelum kita mencoba menyelesaikan rangkaian pertanyaan berikutnya di bawah ini - Anda dapat mencoba melihat beberapa baris dari kumpulan data `trading.prices`:

Contoh data harga Bitcoin:

```sql
SELECT * FROM trading.prices WHERE ticker = 'BTC' LIMIT 5;
```

| ticker | market_date |  price  |  open   |  high   |   low   | volume | change |
| ------ | ----------- | ------- | ------- | ------- | ------- | ------ | ------ |
| BTC    | 2021-08-29  | 48255.0 | 48899.7 | 49621.7 | 48101.9 | 40.96K | -1.31% |
| BTC    | 2021-08-28  | 48897.1 | 49062.8 | 49289.4 | 48428.5 | 36.73K | -0.34% |
| BTC    | 2021-08-27  | 49064.3 | 46830.2 | 49142.0 | 46371.5 | 62.47K | 4.77%  |
| BTC    | 2021-08-26  | 46831.6 | 48994.4 | 49347.8 | 46360.4 | 73.79K | -4.41% |
| BTC    | 2021-08-25  | 48994.5 | 47707.4 | 49230.2 | 47163.3 | 63.54K | 2.68%  |
<br>

Contoh data harga Ethereum:

```sql
SELECT * FROM trading.prices WHERE ticker = 'ETH' LIMIT 5;
```

| ticker | market_date |  price  |  open   |  high   |   low   | volume  | change |
| ------ | ----------- | ------- | ------- | ------- | ------- | ------- | ------ |
| ETH    | 2021-08-29  | 3177.84 | 3243.96 | 3282.21 | 3162.79 | 582.04K | -2.04% |
| ETH    | 2021-08-28  | 3243.90 | 3273.78 | 3284.58 | 3212.24 | 466.21K | -0.91% |
| ETH    | 2021-08-27  | 3273.58 | 3093.78 | 3279.93 | 3063.37 | 839.54K | 5.82%  |
| ETH    | 2021-08-26  | 3093.54 | 3228.03 | 3249.62 | 3057.48 | 118.44K | -4.17% |
| ETH    | 2021-08-25  | 3228.15 | 3172.12 | 3247.43 | 3080.70 | 923.13K | 1.73%  |
<br>

## Kamus Data

| Column Name | Description                     |
| ----------- | ------------------------------- |
| ticker      | salah satu dari BTC atau ETH    |
| market_date | tanggal untuk setiap catatan    |
| price       | harga penutupan di akhir hari   |
| open        | harga pembukaan                 |
| high        | harga tertinggi untuk hari itu  |
| low         | harga terendah untuk hari itu   |
| volume      | total volume yang diperdagangkan|
| change      | % perubahan harga               |
<br>
 
## Pertanyaan Eksplorasi Data

Mari kita jawab beberapa pertanyaan sederhana untuk membantu kita lebih memahami tabel `trading.prices`.

> Ingat untuk membersihkan semua query SQL sebelumnya dari SQLPad sebelum menjalankan setiap query SQL baru!

### Pertanyaan 1

> Berapa total catatan yang kita miliki di tabel `trading.prices`?

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>
<br>

```sql
SELECT
  COUNT(*) AS total_records
FROM trading.prices;
```

</details>
<br>

| total_records |
| ------------- |
|          3404 |
<br>

### Pertanyaan 2

> Berapa banyak catatan per nilai `ticker`?

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>
<br>

```sql
SELECT
  ticker,
  COUNT(*) AS record_count
FROM trading.prices
GROUP BY ticker;
```

</details>
<br>

| ticker | record_count |
| ------ | ------------ |
| BTC    |         1702 |
| ETH    |         1702 |
<br>

### Pertanyaan 3

> Berapa nilai minimum dan maksimum `market_date`?

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>
<br>

```sql
SELECT
  MIN(market_date) AS min_date,
  MAX(market_date) AS max_date
FROM trading.prices;
```

</details>
<br>

|  min_date  |  max_date  |
| ---------- | ---------- |
| 2017-01-01 | 2021-08-29 |
<br>

### Pertanyaan 4

> Apakah ada perbedaan dalam nilai minimum dan maksimum `market_date` untuk setiap ticker?

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>
<br>

```sql
SELECT
  ticker,
  MIN(market_date) AS min_date,
  MAX(market_date) AS max_date
FROM trading.prices
GROUP BY ticker;
```

</details>
<br>

| ticker |  min_date  |  max_date  |
| ------ | ---------- | ---------- |
| BTC    | 2017-01-01 | 2021-08-29 |
| ETH    | 2017-01-01 | 2021-08-29 |
<br>

### Pertanyaan 5

> Berapa rata-rata kolom `price` untuk catatan Bitcoin selama tahun 2020?

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>
<br>

```sql
SELECT
  AVG(price)
FROM trading.prices
WHERE ticker = 'BTC'
  AND market_date BETWEEN '2020-01-01' AND '2020-12-31';
```

</details>
<br>

|        avg         |
| ------------------ |
| 11111.631147540984 |
<br>

### Pertanyaan 6

> Berapa rata-rata bulanan dari kolom `price` untuk Ethereum di tahun 2020? Urutkan outputnya secara kronologis dan bulatkan nilai harga rata-rata ke 2 desimal

<details><summary>Klik di sini untuk melihat solusinya!</summary><br>

```sql
SELECT
  DATE_TRUNC('MON', market_date) AS month_start,
  -- need to cast approx. floats to exact numeric types for round!
  ROUND(AVG(price)::NUMERIC, 2) AS average_eth_price
FROM trading.prices
WHERE EXTRACT(YEAR FROM market_date) = 2020
  AND ticker = 'ETH'
GROUP BY month_start
ORDER BY month_start;
```

</details>
<br>

|      month_start       | average_eth_price |
| ---------------------- | ----------------- |
| 2020-01-01 00:00:00+00 |	156.65           |
| 2020-02-01 00:00:00+00 |	238.76           |
| 2020-03-01 00:00:00+00 |	160.18           |
| 2020-04-01 00:00:00+00 |	171.29           |
| 2020-05-01 00:00:00+00 |	207.45           |
| 2020-06-01 00:00:00+00 |	235.92           |
| 2020-07-01 00:00:00+00 |	259.57           |
| 2020-08-01 00:00:00+00 |	401.73           |
| 2020-09-01 00:00:00+00 |	367.77           |
| 2020-10-01 00:00:00+00 |	375.79           |
| 2020-11-01 00:00:00+00 |	486.73           |
| 2020-12-01 00:00:00+00 |	622.35           |
<br>



### Pertanyaan 7

> Apakah ada nilai `market_date` yang duplikat untuk setiap nilai `ticker` dalam tabel kita?

Saat Anda memeriksa output dari query SQL berikut - apa jawaban akhir Anda?

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>
<br>

```sql
SELECT
  ticker,
  COUNT(market_date) AS total_count,
  COUNT(DISTINCT market_date) AS unique_count
FROM trading.prices
GROUP BY ticker;
```

</details>
<br>

| ticker | total_count | unique_count |
| ------ | ----------- | ------------ |
| BTC    |        1702 |         1702 |
| ETH    |        1702 |         1702 |
<br>

### Pertanyaan 8

> Berapa banyak hari dari tabel `trading.prices` yang ada dimana harga `high` Bitcoin di atas $30,000?

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>
<br>

```sql
SELECT
  COUNT(*) AS row_count
FROM trading.prices
WHERE ticker = 'BTC'
  AND high > 30000;
```

</details>
<br>

| row_count |
| --------- |
|       240 |
<br>

### Pertanyaan 9

> Berapa banyak hari "breakout" yang ada di tahun 2020 dimana kolom `price` lebih besar dari kolom `open` untuk setiap `ticker`?

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>
<br>

```sql
SELECT
  ticker,
  SUM(CASE WHEN price > open THEN 1 ELSE 0 END) AS breakout_days
FROM trading.prices
WHERE DATE_TRUNC('YEAR', market_date) = '2020-01-01'
GROUP BY ticker;
```

</details>
<br>

| ticker | breakout_days |
| ------ | ------------- |
| BTC    |           207 |
| ETH    |           200 |
<br>

### Pertanyaan 10

> Berapa banyak hari "non_breakout" yang ada di tahun 2020 dimana kolom `price` lebih kecil dari kolom `open` untuk setiap `ticker`?

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>
<br>

```sql
SELECT
  ticker,
  SUM(CASE WHEN price < open THEN 1 ELSE 0 END) AS non_breakout_days
FROM trading.prices
-- this another way to specify the year
WHERE market_date >= '2020-01-01' AND market_date <= '2020-12-31'
GROUP BY ticker;
```

</details>
<br>

| ticker | non_breakout_days |
| ------ | ----------------- |
| BTC    |               159 |
| ETH    |               166 |
<br>

### Pertanyaan 11

> Berapa persentase hari di tahun 2020 yang merupakan hari breakout vs non-breakout? Bulatkan persentase ke 2 desimal

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>
<br>

```sql
SELECT
  ticker,
  ROUND(
    SUM(CASE WHEN price > open THEN 1 ELSE 0 END)
      / COUNT(*)::NUMERIC,
    2
  ) AS breakout_percentage,
  ROUND(
    SUM(CASE WHEN price < open THEN 1 ELSE 0 END)
      / COUNT(*)::NUMERIC,
    2
  ) AS non_breakout_percentage
FROM trading.prices
WHERE market_date >= '2020-01-01' AND market_date <= '2020-12-31'
GROUP BY ticker;
```

</details>
<br>

| ticker | breakout_percentage | non_breakout_percentage |
| ------ | ------------------- | ----------------------- |
| BTC    |                0.57 |                    0.43 |
| ETH    |                0.55 |                    0.45 |
<br>

[![forthebadge](./../images/badges/go-to-previous-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step2.md)
[![forthebadge](./../images/badges/go-to-next-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step4.md)

# Lampiran

> Manipulasi Tanggal

Kita menggunakan berbagai manipulasi tanggal di pertanyaan [5](#pertanyaan-5), [6](#pertanyaan-6), [9](#pertanyaan-9) dan [11](#pertanyaan-11) untuk memfilter `trading.prices` hanya untuk nilai tahun 2020.

Ini semua adalah metode yang valid untuk memenuhi syarat nilai `DATE` atau `TIMESTAMP` dalam suatu rentang menggunakan filter `WHERE`:

* `market_date BETWEEN '2020-01-01' AND '2020-12-31'`
* `EXTRACT(YEAR FROM market_date) = 2020`
* `DATE_TRUNC('YEAR', market_date) = '2020-01-01'`
* `market_date >= '2020-01-01' AND market_date <= '2020-12-31'`

Satu-satunya hal tambahan yang perlu diperhatikan adalah bahwa `DATE_TRUNC` mengembalikan tipe data `TIMESTAMP` yang dapat di-cast kembali ke `DATE` biasa menggunakan notasi `::DATE` ketika digunakan dalam query `SELECT`.

> Batasan `BETWEEN`

Catatan tambahan untuk [pertanyaan 5](#pertanyaan-5) - batasan untuk klausa `BETWEEN` harus `tanggal-awal-lebih-dulu` DAN `tanggal-akhir-belakangan`

Lihat apa yang terjadi ketika Anda membalik urutan batasan `DATE` menggunakan query di bawah ini - apakah sesuai dengan ekspektasi Anda?

<details>
  <summary>Klik di sini untuk melihat kode yang "salah"!</summary>
<br>

```sql
SELECT
  AVG(price)
FROM trading.prices
WHERE ticker = 'BTC'
  AND market_date BETWEEN '2020-12-31' AND '2020-01-01';
```

</details>
<br>

> Pembulatan Floats/Doubles

Di PostgreSQL - kita tidak dapat menerapkan fungsi `ROUND` secara langsung ke tipe data perkiraan `FLOAT` atau `DOUBLE PRECISION`.

Sebagai gantinya kita perlu melakukan cast setiap output dari fungsi seperti `AVG` ke tipe data `NUMERIC` yang tepat sebelum kita dapat menggunakannya dengan fungsi perkiraan lainnya seperti `ROUND`

Di [pertanyaan 6](#pertanyaan-6) - jika kita menghapus `::NUMERIC` dari query kita - kita akan mengalami error ini:

```
ERROR:  function round(double precision, integer) does not exist
LINE 3:   ROUND(AVG(price), 2) AS average_eth_price
          ^
HINT:  No function matches the given name and argument types. You might need to add explicit type casts.
```

Anda dapat mencoba ini sendiri dengan menjalankan potongan kode di bawah ini dengan `::NUMERIC` yang dihapus:

<details>
  <summary>Klik di sini untuk melihat kode yang "salah"!</summary>
<br>

```sql
SELECT
  DATE_TRUNC('MON', market_date) AS month_start,
  ROUND(AVG(price), 2) AS average_eth_price
FROM trading.prices
WHERE EXTRACT(YEAR FROM market_date) = 2020
GROUP BY month_start
ORDER BY month_start;
```

</details>
<br>

> Pembagian Bilangan Bulat (Integer Floor Division)

Di [pertanyaan 5](#pertanyaan-5) - ketika membagi nilai dalam SQL, sangat penting untuk mempertimbangkan tipe data dari pembilang (angka di atas) dan penyebut (angka di bawah)

Ketika ada `INTEGER` / `INTEGER` seperti dalam kasus ini - SQL akan menggunakan pembagian `FLOOR` secara default!

Anda dapat mencoba menjalankan query yang sama dengan solusi pertanyaan 5 di atas - tetapi kali ini hapus 2 instance `::NUMERIC` dan pembulatan desimal untuk melihat apa yang terjadi!

Ini adalah kesalahan yang sangat umum ditemukan dalam query SQL dan kami biasanya merekomendasikan untuk melakukan cast pembilang atau penyebut sebagai tipe `NUMERIC` menggunakan sintaks singkat `::NUMERIC` untuk memastikan Anda akan menghindari pembagian bilangan bulat yang ditakuti!

<details>
  <summary>Klik di sini untuk melihat kode yang "salah"!</summary>
<br>

```sql
SELECT
  ticker,
  SUM(CASE WHEN price > open THEN 1 ELSE 0 END) / COUNT(*) AS breakout_percentage,
  SUM(CASE WHEN price < open THEN 1 ELSE 0 END) / COUNT(*) AS non_breakout_percentage
FROM trading.prices
WHERE market_date >= '2019-01-01' AND market_date <= '2019-12-31'
GROUP BY ticker;
```

</details>
<br>
