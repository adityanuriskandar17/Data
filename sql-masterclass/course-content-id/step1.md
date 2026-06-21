<p align="center">
    <img src="./../images/sql-masterclas-banner.png" alt="sql-masterclass-banner">
</p>

[![forthebadge](./../images/badges/version-1.0.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/powered-by-coffee.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/ctrl-c-ctrl-v.svg)]()

# Langkah 1 - Pengantar

## Database Kita

Semua data kita berada dalam sebuah database PostgreSQL dan berisi satu skema bernama `trading`.

Di PostgreSQL, sebuah database dapat berisi banyak skema, dan sebuah skema adalah kumpulan tabel dan objek database lainnya.

## Salin dan Jalankan Sebuah Query SQL

Untuk menjalankan query pertama kita bersama - Anda dapat mengklik sudut kanan atas potongan kode di bawah ini untuk menyalin query `SELECT` dasar ke clipboard Anda.

Anda kemudian dapat menempelkannya ke antarmuka SQLPad Anda dan klik tombol `Run` di pojok kanan atas atau tekan `cmd` + `enter` di Mac atau `control` + `enter` di Windows untuk menjalankan query.

```sql
SELECT * FROM trading.members;
```

Query `SELECT` di atas akan mengembalikan semua catatan dari tabel `members` di dalam skema `trading`.

# Studi Kasus Crypto Kita

Untuk seluruh kursus SQL Simplified ini kita akan fokus pada Studi Kasus SQL Perdagangan Cryptocurrency kita!

## Menetapkan Konteks

Dalam studi kasus fiktif (namun realistis) kami - tim mentor data tepercaya saya dari tim Data With Danny telah berkecimpung di pasar crypto sejak 2017.

Tujuan utama kami untuk studi kasus ini adalah untuk menganalisis kinerja para mentor DWD dari waktu ke waktu dan untuk "memotong dan mengiris" data dalam berbagai cara untuk menyelidiki pertanyaan lain yang mungkin ingin kami jawab!

## Kumpulan Data Kami

Semua data untuk studi kasus ini berada dalam skema `trading` seperti yang telah disebutkan di tutorial sebelumnya.

Ada 3 tabel data yang tersedia untuk kita dalam skema ini yang dapat kita gunakan untuk menjalankan query SQL kita:

1. `members`
2. `prices`
3. `transactions`

Anda dapat memeriksa setiap kumpulan data dengan menyalin potongan kode berikut di bawah ini dan menjalankannya langsung di GUI SQLPad - pastikan untuk menimpa query sebelumnya yang sudah ada di antarmuka SQL!

```sql
SELECT * FROM trading.members;
```

| member_id | first_name |    region     |
| --------- | ---------- | ------------- |
| c4ca42    | Danny      | Australia     |
| c81e72    | Vipul      | United States |
| eccbc8    | Charlie    | United States |
| a87ff6    | Nandita    | United States |
| e4da3b    | Rowan      | United States |
| 167909    | Ayush      | United States |
| 8f14e4    | Alex       | United States |
| c9f0f8    | Abe        | United States |
| 45c48c    | Ben        | Australia     |
| d3d944    | Enoch      | Africa        |
| 6512bd    | Vikram     | India         |
| c20ad4    | Leah       | Asia          |
| c51ce4    | Pavan      | Australia     |
| aab323    | Sonia      | Australia     |
<br>

```sql
SELECT * FROM trading.prices LIMIT 5;
```

| ticker | market_date |  price  |  open   |  high   |   low   | volume  | change |
| ------ | ----------- | ------- | ------- | ------- | ------- | ------- | ------ |
| ETH    | 2021-08-29  | 3177.84 | 3243.96 | 3282.21 | 3162.79 | 582.04K | -2.04% |
| ETH    | 2021-08-28  | 3243.90 | 3273.78 | 3284.58 | 3212.24 | 466.21K | -0.91% |
| ETH    | 2021-08-27  | 3273.58 | 3093.78 | 3279.93 | 3063.37 | 839.54K | 5.82%  |
| ETH    | 2021-08-26  | 3093.54 | 3228.03 | 3249.62 | 3057.48 | 118.44K | -4.17% |
| ETH    | 2021-08-25  | 3228.15 | 3172.12 | 3247.43 | 3080.70 | 923.13K | 1.73%  |
<br>

```sql
SELECT * FROM trading.transactions LIMIT 5;
```

| txn_id | member_id | ticker |  txn_date  | txn_type | quantity | percentage_fee |      txn_time       |
| ------ | --------- | ------ | ---------- | -------- | -------- | -------------- | ------------------- |
|      1 | c81e72    | BTC    | 2017-01-01 | BUY      |       50 |           0.30 | 2017-01-01 00:00:00 |
|      2 | eccbc8    | BTC    | 2017-01-01 | BUY      |       50 |           0.30 | 2017-01-01 00:00:00 |
|      3 | a87ff6    | BTC    | 2017-01-01 | BUY      |       50 |           0.00 | 2017-01-01 00:00:00 |
|      4 | e4da3b    | BTC    | 2017-01-01 | BUY      |       50 |           0.30 | 2017-01-01 00:00:00 |
|      5 | 167909    | BTC    | 2017-01-01 | BUY      |       50 |           0.30 | 2017-01-01 00:00:00 |


Catatan: `LIMIT 5` dalam query di atas akan mengembalikan hanya 5 baris pertama dari setiap kumpulan data.

Ini adalah praktik yang baik untuk selalu menggunakan `LIMIT` pada query Anda untuk berjaga-jaga jika tabelnya sangat besar - Anda tidak ingin mencoba mengembalikan semua 5 juta baris dari tabel besar ketika Anda baru pertama kali memeriksa data!

## Catatan Tentang Skema

Perhatikan di atas bagaimana "`trading.`" disertakan sebelum setiap tabel yang tersedia.

Jika kita menghapusnya - database kita tidak akan dapat menemukan tabel kita.

Query di bawah ini akan mengembalikan error ketika dijalankan:

```sql
SELECT * FROM members;
```

> relation "members" does not exist

Dalam skenario realistis - tabel fisik hampir selalu berada dalam sebuah skema dan kita perlu mereferensikan nama skema untuk menjalankan query kita dengan benar!

[![forthebadge](./../images/badges/go-to-next-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step2.md)
