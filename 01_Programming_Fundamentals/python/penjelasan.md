# Penjelasan: Python untuk Data Engineering

## 1. Perulangan (Loop)

### `for i in range(5):`
```python
for i in range(5):
    print(f"Iterasi ke-{i}")
```

**Apa yang terjadi?**
- `range(5)` membuat urutan angka: 0, 1, 2, 3, 4
- `for i in ...` artinya: untuk setiap angka dalam urutan itu, lakukan sesuatu
- Setiap putaran, nilai `i` berubah: pertama 0, lalu 1, lalu 2, dst
- `print(f"...{i}")` mencetak teks dengan nilai `i`

**Visualisasi:**
```
Putaran 1: i = 0 → cetak "Iterasi ke-0"
Putaran 2: i = 1 → cetak "Iterasi ke-1"
Putaran 3: i = 2 → cetak "Iterasi ke-2"
Putaran 4: i = 3 → cetak "Iterasi ke-3"
Putaran 5: i = 4 → cetak "Iterasi ke-4"
```

**Analogi:** Seperti guru memanggil murid nomor 1 sampai 5. Setiap kali dipanggil, murit itu menjawab.

---

### `while nilai > 0:`
```python
nilai = 50
while nilai > 0:
    print(f"Nilai sekarang: {nilai}")
    nilai -= 10   # artinya: nilai = nilai - 10
```

**Apa yang terjadi?**
- `while nilai > 0:` artinya: ulangi terus SELAMA nilai masih lebih besar dari 0
- `nilai -= 10` artinya kurangi nilai dengan 10 setiap putaran

**Visualisasi:**
```
Nilai awal = 50
Putaran 1: nilai=50, 50>0? Ya → cetak, nilai jadi 40
Putaran 2: nilai=40, 40>0? Ya → cetak, nilai jadi 30
Putaran 3: nilai=30, 30>0? Ya → cetak, nilai jadi 20
Putaran 4: nilai=20, 20>0? Ya → cetak, nilai jadi 10
Putaran 5: nilai=10, 10>0? Ya → cetak, nilai jadi 0
Putaran 6: nilai=0, 0>0? Tidak → STOP
```

**Perbedaan `for` vs `while`:**
- `for` dipakai kalau sudah tahu berapa kali (misal 5x)
- `while` dipakai kalau berhenti berdasarkan kondisi (sampai nilai habis)

---

## 2. Tipe Data

| Tipe | Contoh | Kegunaan |
|------|--------|----------|
| `int` | `25` | Angka bulat |
| `float` | `3.14` | Angka desimal |
| `string` | `"Halo"` | Teks |
| `bool` | `True`/`False` | Ya/Tidak |
| `list` | `[1,2,3]` | Kumpulan data berurutan |
| `dict` | `{"nama":"Budi"}` | Data dengan label |

---

## 3. Fungsi (Function)

### Contoh dari file `basic_python.py`:
```python
def extract_data(file_path: str, delimiter: str = ",") -> list:
    """Membaca file CSV dan mengembalikan list of rows."""
    import csv
    with open(file_path, mode="r") as f:
        reader = csv.reader(f, delimiter=delimiter)
        return [row for row in reader]
```

### Cara Membaca Fungsi:

| Bagian | Arti | Analogi |
|--------|------|---------|
| `def` | Perintah untuk MEMBUAT fungsi | Seperti "definisi" |
| `extract_data` | NAMA fungsi | Nama mesin yang kita buat |
| `(file_path: str, ...)` | PARAMETER / input | Tombol dan lubang input di mesin |
| `-> list` | Tipe OUTPUT yang dikembalikan | Apa yang keluar dari mesin |
| `"""..."""` | DOCSTRING / penjelasan | Buku manual mesin |
| `return` | Nilai yang DIKEMBALIKAN | Hasil keluaran mesin |

### Penjelasan Detail:

**Parameter:**
- `file_path: str` → parameter pertama, bertipe string (teks), berisi alamat file
- `delimiter: str = ","` → parameter kedua, dengan NILAI DEFAULT koma. Kalau dipanggil tanpa nilai ini, otomatis pakai koma

**Cara memanggil fungsi:**
```python
# Panggil dengan 1 parameter (delimiter otomatis pakai default koma)
data = extract_data("data.csv")

# Panggil dengan 2 parameter (delimiter diganti)
data = extract_data("data.tsv", delimiter="\t")
```

**Apa yang terjadi saat fungsi dijalankan:**
1. `open(file_path, mode="r")` → buka file untuk dibaca (`"r"` = read)
2. `csv.reader(f, delimiter=delimiter)` → baca isi file sebagai CSV, pisahkan kolom dengan delimiter
3. `[row for row in reader]` → ubah setiap baris menjadi list, kumpulkan semua baris jadi satu list besar
4. `return ...` → kembalikan hasilnya ke pemanggil fungsi

### Kenapa pakai fungsi?
- **Reusable**: tulis sekali, pakai berkali-kali
- **Terorganisir**: kode tidak berantakan
- **Testing**: mudah diuji per bagian

---

## 4. File I/O (Input/Output)

### Membaca File (`open` dengan mode `"r"`):
```python
with open(file_path, mode="r") as f:
    reader = csv.reader(f, delimiter=delimiter)
    return [row for row in reader]
```

**Apa yang terjadi baris per baris:**

| Baris | Arti |
|-------|------|
| `with open(...) as f:` | Buka file dan beri nama `f`. `with` = otomatis tutup file setelah selesai (tidak perlu manual `.close()`) |
| `mode="r"` | Mode READ (membaca). Mode lain: `"w"` (write/menulis), `"a"` (append/menambah) |
| `csv.reader(f, ...)` | Bungkus file `f` dengan pembaca CSV. Setiap baris akan dipecah menjadi list |
| `[row for row in reader]` | Loop semua baris, kumpulkan jadi satu list |

**Visualisasi file CSV:**
```
Isi file (orders.csv):
order_id,customer,amount
1,Budi,50000
2,Siti,75000

Setelah dibaca csv.reader:
[["order_id", "customer", "amount"],
 ["1", "Budi", "50000"],
 ["2", "Siti", "75000"]]
```

### Menulis File (`open` dengan mode `"w"`):
```python
def write_to_file(data: list, output_path: str):
    with open(output_path, "w") as f:
        for line in data:
            f.write(str(line) + "\n")
```

**Apa yang terjadi:**
1. `open(output_path, "w")` → buka file untuk DITULIS (`"w"` = write). **HATI-HATI**: mode `"w"` akan menghapus isi file lama!
2. `for line in data:` → loop setiap elemen dalam list `data`
3. `f.write(str(line) + "\n")` → tulis baris ke file, tambah baris baru

### Mode-mode `open()`:
| Mode | Arti | File Lama |
|------|------|-----------|
| `"r"` | Read (membaca) | Tidak berubah |
| `"w"` | Write (menulis) | DIHAPUS, ditulis ulang |
| `"a"` | Append (menambah) | Tetap, ditambahkan di akhir |
| `"r+"` | Read + Write | Tidak berubah |

---

## 5. List Comprehension

```python
squares = [x**2 for x in range(10)]
```

**Artinya:** Buat list baru berisi `x` pangkat 2, untuk setiap `x` dari 0 sampai 9.

**Cara baca:** "Buat list kuadrat dari angka 0-9"

Hasil: `[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]`

---

## 6. f-string

```python
print(f"Nilai x adalah {x}")
```

Huruf `f` sebelum string artinya "format string" - kita bisa menyisipkan nilai variabel langsung di dalam kurung kurawal `{}`.

---

## 7. OOP (Object-Oriented Programming) — dari `oop_data_engineer.py`

### 7.1. Apa itu OOP?

OOP adalah cara mengorganisir kode dengan menggabungkan **data** (variabel) dan **perilaku** (fungsi) ke dalam satu "objek".

**Analogi:** Mobil adalah objek. Mobil punya **data** (warna, merek, kecepatan) dan **perilaku** (maju, mundur, belok).

### 7.2. Class dan Object

```python
class DatabaseConnection:
    def __init__(self, host, port, user, password):
        self.host = host
        ...
```

| Istilah | Arti | Analogi |
|---------|------|---------|
| `class` | Cetakan/biru (blueprint) | Cetakan kue |
| `object` | Hasil dari cetakan | Kue jadi |
| `__init__` | Fungsi yang otomatis dijalankan saat objek dibuat | "Pabrik" yang merakit objek |
| `self` | Merujuk ke DIRI SENDIRI | "Aku" punya data sendiri |

**Cara pakai:**
```python
# Buat objek dari class
db = DatabaseConnection("localhost", 5432, "admin", "rahasia")

# Panggil fungsi di dalam objek
db.connect()
```

### 7.3. Encapsulation (Pembungkusan)

```python
class DatabaseConnection:
    def __init__(self, host, port, user, password):
        self.host = host          # public - bisa diakses dari mana saja
        self._user = user         # protected - tanda: hanya untuk internal
        self.__password = password # private - TERSEMBUNYI dari luar
```

**Aturan akses:**
| Prefix | Level | Bisa diakses dari luar? |
|--------|-------|------------------------|
| `self.nama` | Public | Ya |
| `self._nama` | Protected | Sebaiknya tidak (konvensi saja) |
| `self.__nama` | Private | **Tidak** (nama diubah otomatis jadi `_ClassName__nama`) |

**Kenapa penting?** Melindungi data sensitif (password, token) dari kode lain yang tidak berhak.

### 7.4. Inheritance (Pewarisan)

```python
class PostgreSQLConnection(DatabaseConnection):
    def __init__(self, host, port, user, password, database):
        super().__init__(host, port, user, password)  # panggil constructor parent
        self.database = database
```

**Artinya:** `PostgreSQLConnection` adalah anak dari `DatabaseConnection`. Dia punya SEMUA kemampuan parent, plus bisa nambah sendiri.

**Visualisasi:**
```
DatabaseConnection (parent): host, port, user, password, connect()
        ↑
PostgreSQLConnection (child): host, port, user, password, database, connect() [diubah]
```

**`super().__init__(...)`** = panggil constructor milik parent, agar data host/port/user/password tetap terisi.

### 7.5. Polymorphism (method overriding)

```python
class DatabaseConnection:
    def connect(self):
        print(f"Connecting to {self.host}:{self.port}")

class PostgreSQLConnection(DatabaseConnection):
    def connect(self):  # override: tulis ulang fungsi parent
        print(f"Connecting to PostgreSQL at {self.host}:{self.port}/{self.database}")
```

**Artinya:** Fungsi yang SAMA (`connect`) bisa punya perilaku BERBEDA tergantung class-nya.

### 7.6. Abstraction (Abstract Class)

```python
from abc import ABC, abstractmethod

class DataSource(ABC):
    @abstractmethod
    def extract(self):
        pass

    def run_pipeline(self):  # method konkret
        data = self.extract()
        self.load(data)
```

**Artinya:** Membuat "template" yang memaksa class anak untuk mengimplementasikan fungsi tertentu.

- `@abstractmethod` = anak WAJIB mengisi fungsi ini
- `ABC` = class ini tidak bisa dibuat objek langsung, harus ada anaknya

**Kenapa?** Memastikan semua jenis data source (CSV, JSON, API) punya fungsi `extract`, `transform`, `load` yang konsisten.

### 7.7. Contoh Pipeline dengan OOP

```python
pipeline = CSVToPostgresPipeline("input.csv", "users")
pipeline.run_pipeline()
```

Dengan OOP, kita bisa:
- Buat pipeline untuk CSV: `CSVToPostgresPipeline`
- Buat pipeline untuk JSON: `JSONDataSource`
- Buat pipeline untuk API: `APIDataSource`
Semua punya antarmuka yang SAMA (`extract` → `transform` → `load`), tapi isinya BEDA.

---

## 8. Pandas — dari `pandas_intro.py`

### 8.1. Apa itu Pandas?

Pandas adalah library Python untuk **manipulasi data**. Data di pandas disebut **DataFrame** — seperti Excel di Python.

```python
import pandas as pd  # pd adalah singkatan umum untuk pandas
```

### 8.2. DataFrame

DataFrame adalah tabel 2 dimensi (baris × kolom). Mirip dengan:
- Sheet di Excel
- Tabel di SQL
- CSV yang dibuka

```
DataFrame (contoh):
|   | nama  | usia | kota     |
|---|-------|------|----------|
| 0 | Budi  | 25   | Jakarta  |
| 1 | Siti  | 30   | Bandung  |
| 2 | Ali   | 28   | Surabaya |
```

### 8.3. Membaca Data

```python
df = pd.read_csv("data.csv")         # dari CSV
df = pd.read_json("data.json")       # dari JSON
df = pd.read_excel("data.xlsx")      # dari Excel
df = pd.read_parquet("data.parquet") # dari Parquet
```

**Artinya:** "Baca file, ubah jadi DataFrame"

### 8.4. Eksplorasi Data

| Perintah | Hasil |
|----------|-------|
| `df.head()` | 5 baris PERTAMA (cek isi data) |
| `df.info()` | Info kolom: nama, tipe data, jumlah null |
| `df.describe()` | Statistik: mean, min, max, std untuk kolom angka |
| `df.shape` | Ukuran: `(jumlah_baris, jumlah_kolom)` |
| `df.columns` | Daftar semua nama kolom |

### 8.5. Menangani Data Kosong (Missing Values)

```python
df.isnull().sum()  # hitung jumlah null di setiap kolom
```

**Output:**
```
nama     0
usia     2
kota     1
dtype: int64
```

Artinya: kolom `usia` ada 2 baris kosong, `kota` ada 1 baris kosong.

```python
df.dropna(subset=["usia"])  # hapus baris yang kolom usianya null
df.fillna({"usia": df["usia"].median()})  # isi null dengan nilai tengah
```

**Bedanya:**
- `dropna` = HAPUS baris yang kosong
- `fillna` = ISI baris yang kosong dengan nilai tertentu

### 8.6. Transformasi Data

```python
df["tanggal"] = pd.to_datetime(df["tanggal"])       # ubah teks jadi tanggal
df["bulan"] = df["tanggal"].dt.month                # ambil bulan dari tanggal
df["total"] = df["harga"] * df["qty"]               # buat kolom baru dari perkalian
```

**Penjelasan:**
- `pd.to_datetime()` → ubah string "2025-01-15" jadi tipe data tanggal (biar bisa diurutkan, difilter)
- `.dt.month` → ambil angka bulan dari tanggal (Jan=1, Feb=2, ...)
- Membuat kolom baru tinggal tulis `df["nama_kolom_baru"] = rumus`

### 8.7. Group By (Mirip SQL GROUP BY)

```python
summary = df.groupby("kategori").agg({
    "total": ["sum", "mean", "count"],
    "qty": "sum"
})
```

**Artinya:** Kelompokkan data berdasarkan `kategori`, lalu hitung:
- `total` → jumlah (`sum`), rata-rata (`mean`), banyak baris (`count`)
- `qty` → jumlah (`sum`)

**Visualisasi:**
```
Data awal:
| kategori | total | qty |
| Makanan  | 50000 | 2   |
| Minuman  | 30000 | 3   |
| Makanan  | 70000 | 1   |

Setelah groupby("kategori"):
| kategori | total_sum | total_mean | total_count | qty_sum |
| Makanan  | 120000    | 60000      | 2           | 3       |
| Minuman  | 30000     | 30000      | 1           | 3       |
```

`.reset_index()` → ubah `kategori` dari index jadi kolom biasa.

### 8.8. Merge (Mirip SQL JOIN)

```python
df_left  = pd.DataFrame({"id": [1,2,3], "nama": ["A","B","C"]})
df_right = pd.DataFrame({"id": [1,2,4], "skor": [90,80,70]})

inner = pd.merge(df_left, df_right, on="id", how="inner")
```

| `how` | Hasil | Mirip SQL |
|-------|-------|-----------|
| `inner` | Hanya id yang cocok di kedua tabel | INNER JOIN |
| `left` | Semua id dari kiri, kanan diisi NaN jika tidak cocok | LEFT JOIN |
| `outer` | Semua id dari kedua tabel | FULL OUTER JOIN |

**Visualisasi merge `inner`:**
```
 left:          right:           hasil:
| id | nama |  | id | skor |   | id | nama | skor |
| 1  | A    |  | 1  | 90   |→  | 1  | A    | 90   |
| 2  | B    |  | 2  | 80   |→  | 2  | B    | 80   |
| 3  | C    |  | 4  | 70   |   (id 3 & 4 tidak cocok)
```

### 8.9. Menulis Data

```python
df.to_csv("output.csv", index=False)
df.to_parquet("output.parquet", index=False)
```

`index=False` → jangan ikutkan nomor baris ke file output.
