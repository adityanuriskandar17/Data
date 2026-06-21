<p align="center">
    <img src="./../images/sql-masterclas-banner.png" alt="sql-masterclass-banner">
</p>

[![forthebadge](./../images/badges/version-1.0.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/powered-by-coffee.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/ctrl-c-ctrl-v.svg)]()

# Langkah 2 - Menjelajahi Data Members

[![forthebadge](./../images/badges/go-to-previous-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step1.md)
[![forthebadge](./../images/badges/go-to-next-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step3.md)

Sekarang mari kita periksa tabel `trading.members` kita secara lebih mendalam.

## Catatan Tabel

Kita dapat melihat bahwa ada 3 kolom dan 14 baris dalam kumpulan data ini:

`SELECT * FROM trading.members;`

| member_id | first_name |    region      |
| --------- | ---------- | -------------- |
| c4ca42    | Danny      | Australia      |
| c81e72    | Vipul      | United States  |
| eccbc8    | Charlie    | United States  |
| a87ff6    | Nandita    | United States  |
| e4da3b    | Rowan      | United States  |
| 167909    | Ayush      | United States  |
| 8f14e4    | Alex       | United States  |
| c9f0f8    | Abe        | United States  |
| 45c48c    | Ben        | Australia      |
| d3d944    | Enoch      | Africa         |
| 6512bd    | Vikram     | India          |
| c20ad4    | Leah       | Asia           |
| c51ce4    | Pavan      | Australia      |
| aab323    | Sonia      | Australia      |
<br>

## Pengantar SQL Dasar

Mari kita coba jawab beberapa pertanyaan menggunakan kumpulan data ini untuk lebih memahami tim mentor DWD dari tabel `trading.members`.

Setiap pertanyaan memiliki solusi query SQL sendiri yang dapat Anda jalankan untuk menghasilkan output data yang diperlukan.

Semua solusi awalnya disembunyikan - jika Anda petualang, Anda dapat mencoba menjawab setiap pertanyaan tanpa melihat solusinya!

### Bagaimana Cara Menjalankan Contoh Kode Ini?

Buka kodenya, klik sudut kanan atas di GitHub untuk menyalinnya ke clipboard Anda dan tempelkan langsung ke antarmuka SQLPad lalu klik tombol `Run` di pojok kanan atas SQLPad atau tekan `cmd` + `enter` di Mac atau `control` + `enter` di Windows untuk menjalankan query.

> Ingat untuk membersihkan semua query SQL sebelumnya dari SQLPad sebelum menjalankan setiap query SQL baru untuk menghindari benturan dalam output yang dihasilkan!

### Pertanyaan 1

> Tampilkan hanya 5 baris teratas dari tabel `trading.members`

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>

```sql
SELECT * FROM trading.members
LIMIT 5;
```

</details>
<br>

| member_id | first_name |    region     |
| --------- | ---------- | ------------- |
| c4ca42    | Danny      | Australia     |
| c81e72    | Vipul      | United States |
| eccbc8    | Charlie    | United States |
| a87ff6    | Nandita    | United States |
| e4da3b    | Rowan      | United States |
<br>

### Pertanyaan 2

> Urutkan semua baris dalam tabel berdasarkan `first_name` sesuai urutan abjad dan tampilkan 3 baris teratas

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>

```sql
SELECT * FROM trading.members
ORDER BY first_name
LIMIT 3;
```

</details>
<br>

| member_id | first_name |    region     |
| --------- | ---------- | ------------- |
| c9f0f8    | Abe        | United States |
| 8f14e4    | Alex       | United States |
| 167909    | Ayush      | United States |
<br>

### Pertanyaan 3

> Catatan mana dari `trading.members` yang berasal dari region United States?

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>

```sql
SELECT * FROM trading.members
WHERE region = 'United States';
```

</details>
<br>

| member_id | first_name |    region     |
| --------- | ---------- | ------------- |
| c81e72    | Vipul      | United States |
| eccbc8    | Charlie    | United States |
| a87ff6    | Nandita    | United States |
| e4da3b    | Rowan      | United States |
| 167909    | Ayush      | United States |
| 8f14e4    | Alex       | United States |
| c9f0f8    | Abe        | United States |
<br>

### Pertanyaan 4

> Pilih hanya kolom `member_id` dan `first_name` untuk anggota yang tidak berasal dari Australia

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>

```sql
SELECT
  member_id,
  first_name
FROM trading.members
WHERE region != 'Australia';
```

</details>
<br>

| member_id | first_name |
| --------- | ---------- |
| c81e72    | Vipul      |
| eccbc8    | Charlie    |
| a87ff6    | Nandita    |
| e4da3b    | Rowan      |
| 167909    | Ayush      |
| 8f14e4    | Alex       |
| c9f0f8    | Abe        |
| d3d944    | Enoch      |
| 6512bd    | Vikram     |
| c20ad4    | Leah       |
<br>

### Pertanyaan 5

> Kembalikan nilai `region` yang unik dari tabel `trading.members` dan urutkan outputnya berdasarkan urutan abjad terbalik

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>

```sql
SELECT DISTINCT region
FROM trading.members
ORDER BY region DESC;
```

</details>
<br>

|    region     | 
| ------------- |
| United States |
| India         |
| Australia     |
| Asia          |
| Africa        |
<br>

### Pertanyaan 6

> Berapa banyak mentor yang berasal dari Australia atau United States?

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>

```sql
SELECT
  COUNT(*) AS mentor_count
FROM trading.members
WHERE region IN ('Australia', 'United States');
```

</details>
<br>

|  mentor_count |
| ------------- |
|            11 |
<br>

### Pertanyaan 7

> Berapa banyak mentor yang tidak berasal dari Australia atau United States?

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>

```sql
SELECT
  COUNT(*) AS mentor_count
FROM trading.members
WHERE region NOT IN ('Australia', 'United States');
```

</details>
<br>

| mentor_count |
| ------------ |
|            3 |
<br>

### Pertanyaan 8

> Berapa banyak mentor per region? Urutkan output dari region dengan mentor terbanyak hingga paling sedikit

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>

```sql
SELECT
  region,
  COUNT(*) AS mentor_count
FROM trading.members
GROUP BY region
ORDER BY mentor_count DESC;
```

</details>
<br>

|    region     | mentor_count |
| ------------- | ------------ |
| United States |            7 |
| Australia     |            4 |
| India         |            1 |
| Africa        |            1 |
| Asia          |            1 |
<br>

### Pertanyaan 9

> Berapa banyak mentor US dan non US yang ada?

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>

```sql
SELECT
  CASE
    WHEN region != 'United States' THEN 'Non US'
    ELSE region
  END AS mentor_region,
  COUNT(*) AS mentor_count
FROM trading.members
GROUP BY mentor_region
ORDER BY mentor_count DESC;
```

</details>
<br>

| mentor_region | mentor_count |
| ------------- | ------------ |
| United States |            7 |
| Non US        |            7 |
<br>

### Pertanyaan 10

> Berapa banyak mentor yang memiliki nama depan dimulai dengan huruf sebelum `'E'`?

<details>
  <summary>Klik di sini untuk melihat solusinya!</summary>

```sql
SELECT
  COUNT(*) AS mentor_count
FROM trading.members
WHERE LEFT(first_name, 1) < 'E';
```

</details>
<br>

| mentor_count |
| ------------ |
|            6 |
<br>

[![forthebadge](./../images/badges/go-to-previous-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step1.md)
[![forthebadge](./../images/badges/go-to-next-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step3.md)

## Lampiran

> `SELECT *`

Dalam praktiknya - selalu usahakan untuk mengembalikan kolom spesifik yang Anda cari dan gunakan `SELECT *` dengan bijak!

> `LIMIT`

Perhatikan bahwa `LIMIT` terkadang diimplementasikan sebagai `TOP` di beberapa varian database.

Seseorang juga harus berhati-hati saat menggunakan `LIMIT` dengan alat database yang lebih baru seperti BigQuery - meskipun Anda hanya akan mengembalikan jumlah baris yang Anda minta, BQ ditagih berdasarkan jumlah total baris yang dipindai dan `LIMIT` tidak akan menghindari hal ini!

Praktik terbaik adalah selalu menerapkan filter `WHERE` pada partisi tertentu jika memungkinkan untuk mempersempit jumlah data yang harus dipindai - mengurangi biaya query Anda dan mempercepat eksekusi query Anda!

> `!=` atau `<>` untuk "tidak sama dengan"

Anda mungkin telah memperhatikan di pertanyaan 4 dan 9 ada dua metode berbeda untuk menampilkan "tidak sama dengan"

Anda dapat menggunakan `!=` atau `<>` dalam filter `WHERE` untuk mengecualikan catatan.
