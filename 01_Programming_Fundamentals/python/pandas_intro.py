# ============================================
# PANDAS UNTUK DATA ENGINEERING
# ============================================
# Manipulasi data dengan pandas

import pandas as pd
import numpy as np

# --- MEMBACA DATA ---
df = pd.read_csv("data.csv")
df_json = pd.read_json("data.json")
df_excel = pd.read_excel("data.xlsx", sheet_name="Sheet1")
df_parquet = pd.read_parquet("data.parquet")

# --- EKSPLORASI DASAR ---
print(df.head())           # 5 baris pertama
print(df.info())           # info kolom dan tipe data
print(df.describe())       # statistik deskriptif
print(df.shape)            # (baris, kolom)
print(df.columns)          # daftar nama kolom

# --- HANDLE MISSING VALUES ---
df.isnull().sum()                         # jumlah null per kolom
df.dropna(subset=["kolom_penting"])       # hapus baris dgn null di kolom tertentu
df.fillna({"kolom": df["kolom"].median()}) # isi null dengan median

# --- TRANSFORMASI DATA ---
df["tanggal"] = pd.to_datetime(df["tanggal"])
df["bulan"] = df["tanggal"].dt.month
df["kategori_umur"] = np.where(df["umur"] >= 18, "Dewasa", "Anak-anak")
df["total"] = df["harga"] * df["qty"]

# --- GROUP BY & AGGREGASI ---
summary = df.groupby("kategori").agg({
    "total": ["sum", "mean", "count"],
    "qty": "sum"
}).reset_index()

# --- MERGE DATAFRAME ---
df_left = pd.DataFrame({"id": [1, 2, 3], "nama": ["A", "B", "C"]})
df_right = pd.DataFrame({"id": [1, 2, 4], "skor": [90, 80, 70]})

inner = pd.merge(df_left, df_right, on="id", how="inner")
left = pd.merge(df_left, df_right, on="id", how="left")
outer = pd.merge(df_left, df_right, on="id", how="outer")

# --- MENULIS HASIL ---
df.to_csv("output.csv", index=False)
df.to_parquet("output.parquet", index=False)
df.to_json("output.json", orient="records")
