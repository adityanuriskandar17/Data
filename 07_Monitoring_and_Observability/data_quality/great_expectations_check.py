# ============================================
# GREAT EXPECTATIONS - DATA QUALITY
# ============================================
# Validasi kualitas data otomatis
# Bahasa Indonesia

import great_expectations as gx
from great_expectations.dataset import PandasDataset
import pandas as pd

# --- MEMBUAT EXPECTATION SUITE ---
# Expectation Suite adalah kumpulan aturan validasi

# Load data
df = pd.read_parquet("/data/silver/orders.parquet")
dataset = PandasDataset(df)

# --- ATURAN VALIDASI ---

# 1. Kolom tidak boleh null
dataset.expect_column_values_to_not_be_null("order_id")
dataset.expect_column_values_to_not_be_null("customer_id")

# 2. Amount harus positif
dataset.expect_column_values_to_be_between("amount", min_value=0, max_value=1000000)

# 3. Status harus dari daftar tertentu
dataset.expect_column_values_to_be_in_set("status", ["pending", "completed", "cancelled", "refunded"])

# 4. Format email valid
dataset.expect_column_values_to_match_regex("email", r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

# 5. Unik
dataset.expect_column_values_to_be_unique("order_id")

# 6. Tanggal dalam range yang wajar
dataset.expect_column_values_to_be_between(
    "order_date",
    min_value=pd.Timestamp("2020-01-01"),
    max_value=pd.Timestamp("2025-12-31")
)

# 7. Distribusi jumlah baris
dataset.expect_table_row_count_to_be_between(min_value=1000, max_value=10000000)

# --- EKSEKUSI VALIDASI ---
results = dataset.validate()

# --- EVALUASI HASIL ---
if results["success"]:
    print("VALIDASI BERHASIL: Semua data berkualitas baik!")
else:
    print("VALIDASI GAGAL:")

    for result in results["results"]:
        if not result["success"]:
            print(f"  - {result['expectation_config']['expectation_type']}")
            print(f"    Kolom: {result['expectation_config']['kwargs'].get('column', '-')}")
            print(f"    Baris gagal: {result['result'].get('unexpected_count', 0)}")

# --- SAVE EXPECTATION SUITE UNTUK REUSE ---
# Digunakan di production untuk validasi otomatis
expectation_suite = dataset.get_expectation_suite(discard_failed_expectations=False)
# context.save_expectation_suite(expectation_suite, "orders_suite.json")
