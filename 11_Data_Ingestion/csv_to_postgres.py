# ============================================
# CSV → POSTGRESQL — INGESTION
# ============================================
# Membaca CSV (termasuk file besar) dan INSERT ke PostgreSQL
#
# Teknik untuk large data:
# 1. Chunking: baca file dalam potongan (chunk)
# 2. Batch INSERT: insert banyak baris sekaligus
# 3. COPY (paling cepat): gunakan COPY dari PostgreSQL
# 4. Progress bar: tracking progress untuk file besar

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from sqlalchemy import create_engine
import os
import time
import argparse

# --- KONFIGURASI DATABASE ---
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "user": os.getenv("DB_USER", "bosani"),
    "password": os.getenv("DB_PASSWORD", "1234567890"),
    "database": os.getenv("DB_NAME", "latihan_de"),
}

DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


# ============================================
# METODE 1: Pandas + SQLAlchemy (chunking)
# ============================================
# Cocok untuk: file < 1 GB, sudah punya pandas di pipeline
# Kelebihan: sederhana, fleksibel untuk transformasi
# Kekurangan: lebih lambat dari COPY, butuh memory untuk tiap chunk

def csv_to_postgres_pandas(
    csv_path: str,
    table_name: str,
    chunksize: int = 10000,
    if_exists: str = "append"
):
    """
    Baca CSV dalam chunk, insert ke PostgreSQL via SQLAlchemy.
    
    Args:
        csv_path: path ke file CSV
        table_name: nama tabel target (schema.table)
        chunksize: jumlah baris per batch
        if_exists: 'append', 'replace', 'fail'
    """
    print(f"\n{'='*50}")
    print(f"METODE PANDAS: {csv_path} -> {table_name}")
    print(f"{'='*50}")

    engine = create_engine(DATABASE_URL)
    start = time.time()
    total_rows = 0

    # Baca CSV dalam chunk
    for i, chunk in enumerate(pd.read_csv(csv_path, chunksize=chunksize)):
        chunk.to_sql(
            name=table_name,
            con=engine,
            if_exists=if_exists if i == 0 else "append",
            index=False,
            method="multi"  # multi-row insert (lebih cepat)
        )
        total_rows += len(chunk)
        elapsed = time.time() - start
        rate = total_rows / elapsed if elapsed > 0 else 0
        print(f"  Chunk {i+1}: {len(chunk)} rows inserted | "
              f"Total: {total_rows} | "
              f"Rate: {rate:.0f} rows/s")

    elapsed = time.time() - start
    print(f"✅ Selesai: {total_rows} rows in {elapsed:.1f}s ({total_rows/elapsed:.0f} rows/s)")
    engine.dispose()


# ============================================
# METODE 2: COPY (paling cepat untuk large data)
# ============================================
# Menggunakan COPY FROM PostgreSQL — format CSV native
# Cocok untuk: file > 1 GB, produksi
# Kelebihan: TERCEPAT (10-100x lebih cepat dari INSERT)
# Kekurangan: tidak bisa transformasi saat load

def csv_to_postgres_copy(
    csv_path: str,
    table_name: str,
    delimiter: str = ",",
    has_header: bool = True
):
    """
    Load CSV ke PostgreSQL menggunakan COPY (paling cepat).
    
    Args:
        csv_path: path ke file CSV
        table_name: nama tabel target
        delimiter: delimiter CSV
        has_header: apakah CSV punya header
    """
    print(f"\n{'='*50}")
    print(f"METODE COPY: {csv_path} -> {table_name}")
    print(f"{'='*50}")

    conn = psycopg2.connect(**DB_CONFIG)
    start = time.time()

    with conn.cursor() as cur:
        with open(csv_path, "r") as f:
            if has_header:
                next(f)  # skip header

            # COPY FROM — native PostgreSQL, sangat cepat
            cur.copy_from(
                file=f,
                table=table_name.split(".")[0] if "." in table_name else None,
                sep=delimiter,
                columns=None,  # semua kolom sesuai urutan CSV
            )

    conn.commit()

    # Hitung rows
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        total_rows = cur.fetchone()[0]

    conn.close()
    elapsed = time.time() - start
    file_size_mb = os.path.getsize(csv_path) / (1024 * 1024)
    print(f"✅ COPY selesai: {total_rows} rows, {file_size_mb:.0f} MB")
    print(f"   Waktu: {elapsed:.1f}s ({total_rows/elapsed:.0f} rows/s)")


# ============================================
# METODE 3: Batch INSERT (psycopg2 execute_values)
# ============================================
# Cocok untuk: perlu validasi/transformasi sebelum insert
# Lebih cepat dari pandas, lebih lambat dari COPY

def csv_to_postgres_batch(
    csv_path: str,
    table_name: str,
    batch_size: int = 5000
):
    """
    Baca CSV chunk-by-chunk, insert pakai batch INSERT.
    Memberi kontrol penuh atas data sebelum insert.
    """
    print(f"\n{'='*50}")
    print(f"METODE BATCH INSERT: {csv_path} -> {table_name}")
    print(f"{'='*50}")

    conn = psycopg2.connect(**DB_CONFIG)
    start = time.time()
    total_rows = 0

    # Baca CSV
    for i, chunk in enumerate(pd.read_csv(csv_path, chunksize=batch_size)):
        # --- Transformasi/contoh validasi sebelum insert ---
        # Hapus baris dengan nilai null
        chunk = chunk.dropna(subset=["customer_id", "total_amount"], how="any")

        # Filter hanya amount positif
        if "total_amount" in chunk.columns:
            chunk = chunk[chunk["total_amount"] > 0]

        if len(chunk) == 0:
            continue

        # Convert ke list of tuples untuk execute_values
        columns = list(chunk.columns)
        values = [tuple(row) for row in chunk.to_numpy()]

        with conn.cursor() as cur:
            execute_values(
                cur,
                f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s",
                values,
                page_size=batch_size
            )
        conn.commit()

        total_rows += len(chunk)
        elapsed = time.time() - start
        print(f"  Batch {i+1}: {len(chunk)} rows | Total: {total_rows}")

    conn.close()
    elapsed = time.time() - start
    print(f"✅ Batch INSERT: {total_rows} rows in {elapsed:.1f}s")


# ============================================
# MAIN — Pilih metode berdasarkan ukuran file
# ============================================

def auto_ingest(csv_path: str, table_name: str):
    """Pilih metode otomatis berdasarkan ukuran file."""
    file_size_mb = os.path.getsize(csv_path) / (1024 * 1024)
    print(f"File size: {file_size_mb:.1f} MB")

    if file_size_mb < 100:
        print("→ File kecil: pakai Pandas chunking")
        csv_to_postgres_pandas(csv_path, table_name)
    elif file_size_mb < 1000:
        print("→ File sedang: pakai Batch INSERT (dengan validasi)")
        csv_to_postgres_batch(csv_path, table_name)
    else:
        print("→ File BESAR: pakai COPY (tercepat)")
        csv_to_postgres_copy(csv_path, table_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSV to PostgreSQL Ingestion")
    parser.add_argument("csv", nargs="?", help="Path ke file CSV")
    parser.add_argument("--table", default="ingestion.orders", help="Nama tabel target")
    parser.add_argument("--method", choices=["auto", "pandas", "copy", "batch"], default="auto")
    parser.add_argument("--chunksize", type=int, default=10000)
    args = parser.parse_args()

    if args.csv:
        csv_path = args.csv
    else:
        # Default: cari CSV terbesar di folder data/
        csv_files = sorted(
            [f for f in os.listdir(DATA_DIR) if f.endswith(".csv") and f != "products.csv"],
            key=lambda f: os.path.getsize(os.path.join(DATA_DIR, f)),
            reverse=True
        )
        if not csv_files:
            print("❌ Tidak ada CSV di folder data/. Jalankan generate_data.py dulu.")
            exit(1)
        csv_path = os.path.join(DATA_DIR, csv_files[0])
        print(f"Default: {csv_path}")

    if args.method == "auto":
        auto_ingest(csv_path, args.table)
    elif args.method == "pandas":
        csv_to_postgres_pandas(csv_path, args.table, args.chunksize)
    elif args.method == "copy":
        csv_to_postgres_copy(csv_path, args.table)
    elif args.method == "batch":
        csv_to_postgres_batch(csv_path, args.table)
