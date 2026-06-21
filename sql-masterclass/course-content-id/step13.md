<p align="center">
    <img src="./../images/sql-masterclas-banner.png" alt="sql-masterclass-banner">
</p>

[![forthebadge](./../images/badges/version-1.0.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/powered-by-coffee.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)]()
[![forthebadge](https://forthebadge.com/images/badges/ctrl-c-ctrl-v.svg)]()

# Ringkasan SQL Masterclass

[![forthebadge](./../images/badges/go-to-previous-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step12.md)
[![forthebadge](./../images/badges/go-to-next-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/the-end.md)

Selamat, Anda telah mencapai akhir dari SQL Masterclass ini!

Berikut adalah beberapa topik yang telah Anda pelajari dalam kursus SQL Masterclass yang singkat namun padat ini:

> Langkah 2: Memeriksa tabel `trading.members`

* Memilih baris dan kolom dari tabel database dengan `SELECT`
* Menggunakan `LIMIT` untuk hanya mengembalikan sejumlah baris tertentu dari query
* Menghitung jumlah record menggunakan `COUNT(*)`
* Menghitung jumlah record kolom dan tabel unik menggunakan `COUNT(DISTINCT)`
* Menyaring data menggunakan filter `WHERE`
* Memilih rentang `DATE` menggunakan `BETWEEN`, `>`, `>=`, `<`, `<=`
* Menggunakan kondisi filter `IN` dan `NOT IN` untuk menghapus dan menyimpan record
* Menggunakan `CASE WHEN` untuk menerapkan logika if-else sederhana ke kolom yang ada

> Langkah 3: Menganalisis harga harian BTC dan ETH di tabel `trading.prices`

* Menemukan tanggal `MIN` dan `MAX`
* Menggunakan `GROUP BY` untuk mengagregasi data di berbagai level untuk analisis
* Mengekstrak informasi dari tanggal menggunakan `DATE_TRUNC` dan `EXTRACT`
* Menggunakan `DATE_TRUNC` untuk mendapatkan tanggal awal bulan dari sebuah `DATE`
* Menggunakan `AVG` untuk mencari harga rata-rata
* Mengubah tipe data float menjadi `NUMERIC` yang tepat untuk digunakan dengan fungsi `ROUND`
* Menggunakan kondisi `AND` untuk menerapkan beberapa aturan logis untuk filter `WHERE`
* Menggunakan `SUM CASE WHEN` untuk mengagregasi nilai logis mirip dengan COUNTIF di Excel
* Mengubah tipe data `INTEGER` menjadi `NUMERIC` untuk menghindari kesalahan pembagian integer floor

> Langkah 4: Melihat semua riwayat transaksi di tabel `trading.transactions`

* Penggunaan lebih lanjut dari `SUM CASE WHEN` untuk mereplikasi fungsionalitas SUMIF di Excel
* Cara menyaring record dari hasil `GROUP BY` menggunakan klausa `HAVING`
* Menggunakan CTE dan subquery untuk melakukan penyaringan hasil yang sama
* Menggunakan fungsi window `RANK` untuk melakukan pengurutan khusus untuk kumpulan hasil

> Langkah 5: Memulai analisis data

* Menginterpretasikan diagram hubungan entitas (ERD) untuk memvisualisasikan penggabungan tabel
* Menganalisis rentang data untuk memastikan periode analisis selaras
* Melakukan `INNER JOIN` untuk menggabungkan dataset guna memilih kolom dari kedua tabel
* Menggabungkan CTE dan join untuk query bertahap
* Menggabungkan beberapa fungsi agregasi untuk menghasilkan output tabel yang lebih besar

> Langkah 6-7: Perencanaan ke depan dan menggunakan tabel dasar untuk analisis data

* Menghapus dan membuat tabel sementara untuk digunakan kembali dalam query SQL di masa depan
* Menambahkan `INTERVAL` waktu ke suatu tanggal
* Menggunakan pernyataan `ALTER` dan `UPDATE` untuk memanipulasi tabel sementara yang ada
* Menggunakan klausa `WINDOW FRAME` kustom untuk menentukan jendela geser untuk metrik kumulatif
* Menggunakan fungsi window `SUM` untuk menghitung nilai penyebut untuk kalkulasi persentase
* Menggunakan `MAX CASE WHEN` untuk memutar data dari format panjang ke lebar

> Langkah 8-12: Skenario Studi Kasus Akhir

* Membuat skenario data yang disederhanakan untuk lebih memahami setiap pertanyaan
* Menerapkan agregasi `SUM PRODUCT` untuk menghitung investasi awal
* Melakukan beberapa join ke tabel yang sama dengan kondisi join yang berbeda
* Mengalikan banyak kolom untuk menghasilkan biaya berdasarkan persentase
* Menghitung skenario hipotetis dan menerapkan logika kompleks menggunakan SQL
* Membuat alur kerja CTE lengkap untuk menghasilkan dataset pelaporan
* Mengagregasi data di beberapa level untuk menghasilkan banyak wawasan

[![forthebadge](./../images/badges/go-to-previous-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/step12.md)
[![forthebadge](./../images/badges/go-to-next-tutorial.svg)](https://github.com/datawithdanny/sql-masterclass/tree/main/course-content/the-end.md)
