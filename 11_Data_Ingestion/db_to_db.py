# ============================================
# DATABASE A → DATABASE B — TRANSFER
# ============================================
# Mentransfer data antar database:
# 1. PostgreSQL → PostgreSQL (server berbeda)
# 2. PostgreSQL → PostgreSQL (server sama, schema beda)
# 3. Dengan transformasi di tengah jalan
# 4. Large data: batch + parallel transfer

import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
from sqlalchemy import create_engine
import time
import os
import argparse
import threading
from datetime import datetime

# ============================================
# KONFIGURASI — Sesuaikan dengan environment
# ============================================

# Database SUMBER (A)
SOURCE_DB = {
    "host": os.getenv("SRC_HOST", "localhost"),
    "port": int(os.getenv("SRC_PORT", "5432")),
    "user": os.getenv("SRC_USER", "bosani"),
    "password": os.getenv("SRC_PASSWORD", "1234567890"),
    "database": os.getenv("SRC_DB", "latihan_de"),
}

# Database TUJUAN (B)
TARGET_DB = {
    "host": os.getenv("TGT_HOST", "localhost"),
    "port": int(os.getenv("TGT_PORT", "5432")),
    "user": os.getenv("TGT_USER", "bosani"),
    "password": os.getenv("TGT_PASSWORD", "1234567890"),
    "database": os.getenv("TGT_DB", "latihan_de"),
}

SOURCE_URL = f"postgresql://{SOURCE_DB['user']}:{SOURCE_DB['password']}@{SOURCE_DB['host']}:{SOURCE_DB['port']}/{SOURCE_DB['database']}"
TARGET_URL = f"postgresql://{TARGET_DB['user']}:{TARGET_DB['password']}@{TARGET_DB['host']}:{TARGET_DB['port']}/{TARGET_DB['database']}"


# ============================================
# METODE 1: Extract → Transform → Load (ETL)
# ============================================
# Paling sederhana: baca dari A, transform, tulis ke B
# Cocok untuk: data < 10 juta baris

def db_to_db_etl(
    source_query: str,
    target_table: str,
    transform_fn=None,
    chunksize: int = 50000
):
    """
    Transfer data dari database A ke B dengan transformasi opsional.

    Args:
        source_query: SQL query di database sumber
        target_table: nama tabel target (schema.table)
        transform_fn: fungsi transformasi (DataFrame -> DataFrame)
        chunksize: jumlah baris per batch
    """
    print(f"\n{'='*50}")
    print(f"DB-TO-DB ETL")
    print(f"  Source: {SOURCE_DB['database']}@{SOURCE_DB['host']}")
    print(f"  Target: {TARGET_DB['database']}@{TARGET_DB['host']}")
    print(f"  Query: {source_query[:80]}...")
    print(f"{'='*50}")

    source_engine = create_engine(SOURCE_URL)
    target_engine = create_engine(TARGET_URL)
    start = time.time()
    total_rows = 0

    for i, chunk in enumerate(pd.read_sql(source_query, source_engine, chunksize=chunksize)):
        if len(chunk) == 0:
            continue

        # Transformasi (jika ada)
        if transform_fn:
            chunk = transform_fn(chunk)

        # Tulis ke target
        chunk.to_sql(
            name=target_table,
            con=target_engine,
            if_exists="replace" if i == 0 else "append",
            index=False,
            method="multi"
        )

        total_rows += len(chunk)
        elapsed = time.time() - start
        print(f"  Batch {i+1}: {len(chunk)} rows | Total: {total_rows} | {elapsed:.1f}s")

    elapsed = time.time() - start
    source_engine.dispose()
    target_engine.dispose()
    print(f"✅ Transfer selesai: {total_rows} rows in {elapsed:.1f}s")


# ============================================
# METODE 2: Batch INSERT (psycopg2, lebih cepat)
# ============================================
# Langsung streaming dari source cursor ke target
# Tidak perlu pandas DataFrame di memory

def db_to_db_streaming(
    source_query: str,
    target_table: str,
    target_columns: list = None,
    batch_size: int = 5000
):
    """
    Transfer data antar database menggunakan streaming cursor.
    Data langsung dialirkan dari source ke target tanpa disimpan di memory.
    """
    print(f"\n{'='*50}")
    print(f"DB-TO-DB STREAMING")
    print(f"  Source -> Target (streaming, no intermediate)")

    src_conn = psycopg2.connect(**SOURCE_DB)
    tgt_conn = psycopg2.connect(**TARGET_DB)
    start = time.time()
    total_rows = 0

    with src_conn.cursor(name="stream_cursor") as src_cur:
        src_cur.execute(source_query)

        columns = target_columns or [desc[0] for desc in src_cur.description]
        col_names = ", ".join(columns)

        while True:
            rows = src_cur.fetchmany(batch_size)
            if not rows:
                break

            with tgt_conn.cursor() as tgt_cur:
                execute_values(
                    tgt_cur,
                    f"INSERT INTO {target_table} ({col_names}) VALUES %s",
                    rows,
                    page_size=batch_size
                )
            tgt_conn.commit()

            total_rows += len(rows)
            if total_rows % 50000 == 0:
                elapsed = time.time() - start
                print(f"  {total_rows} rows transferred... ({elapsed:.1f}s)")

    src_conn.close()
    tgt_conn.close()
    elapsed = time.time() - start
    print(f"✅ Streaming transfer: {total_rows} rows in {elapsed:.1f}s")
    print(f"   Rate: {total_rows/elapsed:.0f} rows/s")


# ============================================
# METODE 3: Parallel Partition Transfer
# ============================================
# Untuk data SANGAT BESAR: transfer secara paralel
# Membagi data berdasarkan range ID, transfer simultan

def _transfer_partition(
    source_query: str,
    target_table: str,
    columns: list,
    partition_name: str
):
    """Transfer satu partisi (dipanggil oleh thread)."""
    try:
        src_conn = psycopg2.connect(**SOURCE_DB)
        tgt_conn = psycopg2.connect(**TARGET_DB)

        with src_conn.cursor(name=f"cur_{partition_name}") as src_cur:
            src_cur.execute(source_query)
            col_names = ", ".join(columns)

            while True:
                rows = src_cur.fetchmany(5000)
                if not rows:
                    break
                with tgt_conn.cursor() as tgt_cur:
                    execute_values(
                        tgt_cur,
                        f"INSERT INTO {target_table} ({col_names}) VALUES %s",
                        rows,
                        page_size=5000
                    )
                tgt_conn.commit()

        src_conn.close()
        tgt_conn.close()
        print(f"  ✅ Thread {partition_name}: selesai")
    except Exception as e:
        print(f"  ❌ Thread {partition_name}: {e}")


def db_to_db_parallel(
    source_table: str,
    target_table: str,
    id_column: str = "order_id",
    num_threads: int = 4
):
    """
    Transfer antar database secara paralel.
    Data dibagi berdasarkan range ID.
    """
    print(f"\n{'='*50}")
    print(f"DB-TO-DB PARALLEL ({num_threads} threads)")
    print(f"{'='*50}")

    start = time.time()

    # Dapatkan range ID
    src_conn = psycopg2.connect(**SOURCE_DB)
    with src_conn.cursor() as cur:
        cur.execute(f"SELECT MIN({id_column}), MAX({id_column}) FROM {source_table}")
        min_id, max_id = cur.fetchone()
        cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_schema='ingestion' AND table_name='{source_table.split('.')[1]}' ORDER BY ordinal_position")
        columns = [row[0] for row in cur.fetchall()]
    src_conn.close()

    if not min_id or not max_id:
        print("❌ Tabel kosong")
        return

    # Bagi range per thread
    chunk_size = (max_id - min_id + 1) // num_threads
    threads = []

    for i in range(num_threads):
        start_id = min_id + (i * chunk_size)
        end_id = start_id + chunk_size - 1 if i < num_threads - 1 else max_id

        query = f"""
            SELECT * FROM {source_table}
            WHERE {id_column} BETWEEN {start_id} AND {end_id}
            ORDER BY {id_column}
        """

        thread = threading.Thread(
            target=_transfer_partition,
            args=(query, target_table, columns, f"part{i+1}")
        )
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()

    elapsed = time.time() - start
    print(f"✅ Parallel transfer selesai dalam {elapsed:.1f}s")


# ============================================
# METODE 4: Dengan Transformasi Agregasi
# ============================================
# Contoh: source tabel orders → target tabel summary

def transform_orders_to_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Contoh transformasi: orders → daily summary."""
    df["order_date"] = pd.to_datetime(df["order_date"]).dt.date
    summary = df.groupby(["order_date", "category"]).agg(
        total_orders=("order_id", "count"),
        total_revenue=("total_amount", "sum"),
        avg_order_value=("total_amount", "mean")
    ).reset_index()
    return summary


def transfer_with_aggregation():
    """Transfer + agregasi: orders -> daily_summary."""
    print("Transfer data dengan agregasi...")
    db_to_db_etl(
        source_query="SELECT * FROM ingestion.orders WHERE status = 'delivered'",
        target_table="ingestion_dest.orders_summary",
        transform_fn=transform_orders_to_summary
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Database A to Database B Transfer")
    parser.add_argument("--method", choices=["etl", "stream", "parallel", "agg"], default="stream")
    parser.add_argument("--source-query", default="SELECT * FROM ingestion.orders ORDER BY order_id")
    parser.add_argument("--target-table", default="ingestion_dest.orders_summary")
    parser.add_argument("--table", help="Nama tabel source (untuk parallel)")
    parser.add_argument("--threads", type=int, default=4)
    args = parser.parse_args()

    if args.method == "etl":
        db_to_db_etl(args.source_query, args.target_table)
    elif args.method == "stream":
        db_to_db_streaming(args.source_query, args.target_table)
    elif args.method == "parallel":
        table = args.table or "ingestion.orders"
        db_to_db_parallel(table, args.target_table, num_threads=args.threads)
    elif args.method == "agg":
        transfer_with_aggregation()
