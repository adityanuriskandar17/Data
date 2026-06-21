# ============================================
# BASIC PYTHON UNTUK DATA ENGINEERING
# ============================================
# Materi: Tipe data, kontrol flow, fungsi, file I/O

# --- TIPE DATA DASAR ---
nama = "Data Engineer"       # string
usia = 25                     # integer
tinggi = 175.5                # float
is_employed = True            # boolean

# --- STRUKTUR DATA ---
list_data = [1, 2, 3, 4, 5]
tuple_data = (1, 2, 3)
set_data = {1, 2, 3, 3, 3}    # {1, 2, 3} - duplikat otomatis dihapus
dict_data = {"nama": "Budi", "usia": 30}

# --- KONTROL FLOW ---
nilai = 85
if nilai >= 90:
    grade = "A"
elif nilai >= 80:
    grade = "B"
else:
    grade = "C"

# --- LOOPING ---
for i in range(5):
    print(f"Iterasi ke-{i}")

while nilai > 0:
    nilai -= 10

# list comprehension
squares = [x**2 for x in range(10)]

# --- FUNGSI ---
def extract_data(file_path: str, delimiter: str = ",") -> list:
    """Membaca file CSV dan mengembalikan list of rows."""
    import csv
    with open(file_path, mode="r") as f:
        reader = csv.reader(f, delimiter=delimiter)
        return [row for row in reader]

# --- FILE I/O ---
def write_to_file(data: list, output_path: str):
    with open(output_path, "w") as f:
        for line in data:
            f.write(str(line) + "\n")

# --- ERROR HANDLING ---
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Tidak bisa membagi dengan nol!")
finally:
    print("Blok ini selalu dijalankan.")
