# Penjelasan: SQL untuk Data Engineering

## 1. Apa itu SQL?
SQL (Structured Query Language) adalah bahasa untuk berbicara dengan database. Bayangkan database seperti Excel raksasa, dan SQL adalah cara kita menyuruh Excel itu melakukan sesuatu.

## 2. Jenis Perintah SQL

### DDL (Data Definition Language)
Membuat/mengubah struktur tabel.
```sql
CREATE TABLE customers (...);   -- Buat tabel baru
ALTER TABLE ... ADD COLUMN ...; -- Tambah kolom
DROP TABLE ...;                 -- Hapus tabel
```

### DML (Data Manipulation Language)
Memasukkan/mengubah/menghapus data.
```sql
INSERT INTO ... VALUES ...;  -- Tambah baris baru
UPDATE ... SET ... WHERE ...;-- Ubah data yang sudah ada
DELETE FROM ... WHERE ...;   -- Hapus baris tertentu
```

### DQL (Data Query Language)
Mengambil data (SELECT).
```sql
SELECT ... FROM ... WHERE ...;  -- Ambil data dengan filter
```

---

## 3. SELECT - Mengambil Data

```sql
SELECT * FROM customers;
```
- `SELECT` = ambil
- `*` = semua kolom
- `FROM customers` = dari tabel customers
- **Artinya:** Ambil SEMUA kolom dari tabel customers

```sql
SELECT name, email FROM customers WHERE customer_id = 1;
```
**Artinya:** Ambil kolom `name` dan `email` SAJA, dari tabel customers, TAPI hanya baris yang customer_id-nya 1.

---

## 4. JOIN - Menggabungkan Data

Bayangkan dua tabel:
- `customers`: berisi data pelanggan
- `orders`: berisi data pesanan

```sql
SELECT c.name, o.order_date
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;
```

**Visualisasi:**
```
Tabel customers:          Tabel orders:
| id | name  |           | id | customer_id | order_date |
| 1  | Budi  |           | 1  | 1           | 2025-01-01 |
| 2  | Siti  |           | 2  | 1           | 2025-01-02 |
                           | 3  | 2           | 2025-01-03 |

Hasil JOIN:
| name  | order_date |
| Budi  | 2025-01-01 |
| Budi  | 2025-01-02 |
| Siti  | 2025-01-03 |
```

### Jenis JOIN:
- `INNER JOIN`: hanya data yang cocok di kedua tabel
- `LEFT JOIN`: semua data dari tabel kiri, yang kanan diisi NULL jika tidak cocok
- `RIGHT JOIN`: kebalikan LEFT
- `FULL JOIN`: semua data dari kedua tabel

---

## 5. GROUP BY - Mengelompokkan

```sql
SELECT status, COUNT(*) AS jumlah
FROM orders
GROUP BY status;
```

**Artinya:** Kelompokkan pesanan berdasarkan statusnya, lalu hitung berapa banyak setiap kelompok.

Hasil:
| status | jumlah |
|--------|--------|
| pending | 50 |
| completed | 200 |
| cancelled | 10 |

**Seperti:** "Hitung berapa banyak pesanan yang pending, completed, dan cancelled."

---

## 6. Perbedaan WHERE vs HAVING

- `WHERE`: filter SEBELUM data dikelompokkan
- `HAVING`: filter SETELAH data dikelompokkan

```sql
SELECT status, COUNT(*) AS jumlah
FROM orders
WHERE order_date > '2025-01-01'  -- filter baris dulu
GROUP BY status
HAVING COUNT(*) > 5;              -- filter hasil group
```

---

## 7. Indeks (Index)

```sql
CREATE INDEX idx_customer_id ON orders(customer_id);
```

**Apa itu Index?** Seperti daftar isi di buku. Tanpa index, untuk mencari data harus baca seluruh tabel. Dengan index, database langsung tahu di mana data berada.

- Index mempercepat SELECT
- Index memperlambat INSERT/UPDATE (karena harus update index juga)
- Pakai index untuk kolom yang sering di-filter (`WHERE`, `JOIN`)
