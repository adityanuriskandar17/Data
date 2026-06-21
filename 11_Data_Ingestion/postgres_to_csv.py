# ============================================
# POSTGRESQL → CSV — EXPORT
# ============================================
# Export data dari PostgreSQL ke CSV
#
# Teknik untuk large data:
# 1. Server-side COPY: export langsung dari server (tercepat)
# 2. Streaming cursor: baca row-by-row tanpa muat semua ke memory
# 3. Chunked export: pecah file besar jadi beberapa file kecil
# 4. Parallel export: export beberapa tabel sekaligus

import psycopg2
import os
import time
import argparse
import csv
import threading
from datetime import datetime

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "user": os.getenv("DB_USER", "bosani"),
    "password": os.getenv("DB_PASSWORD", "1234567890"),
    "database": os.getenv("DB_NAME", "latihan_de"),
}

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "exports")


# ============================================
# METODE 1: COPY TO (server-side, TERCEPAT)
# ============================================
# PostgreSQL langsung menulis file CSV di SERVER
# Cocok untuk: file > 1 GB, production
# Catatan: file ditulis di server PostgreSQL, bukan di lokal

def export_copy_to(query: str, output_path: str, delimiter: str = ","):
    """
    Export menggunakan COPY TO — ditulis di server PostgreSQL.
    
    Args:
        query: SQL query (SELECT ... atau nama tabel)
        output_path: path output di SERVER PostgreSQL
    """
    print(f"\n{'='*50}")
    print(f"COPY TO (server): {output_path}")
    print(f"{'='*50}")

    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    start = time.time()

    with conn.cursor() as cur:
        sql = f"COPY ({query}) TO '{output_path}' DELIMITER '{delimiter}' CSV HEADER;"
        cur.execute(sql)

    conn.close()
    elapsed = time.time() - start
    print(f"✅ COPY TO selesai dalam {elapsed:.1f}s")
    print(f"   File di server: {output_path}")


# ============================================
# METODE 2: Streaming cursor + CSV Writer (client-side)
# ============================================
# Data tidak dimuat ke memory — langsung stream ke file
# Cocok untuk: file besar, ingin file di lokal

def export_streaming(
    query: str,
    output_path: str,
    fetch_size: int = 1000
):
    """
    Export dengan server-side cursor (streaming).
    Data dibaca dalam batch, ditulis ke file CSV.
    Memory aman untuk data berapa pun besarnya.
    """
    print(f"\n{'='*50}")
    print(f"STREAMING EXPORT: {output_path}")
    print(f"{'='*50}")

    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True  # penting untuk server-side cursor
    start = time.time()
    total_rows = 0

    with conn.cursor(name="export_cursor") as cur:
        cur.execute(query)

        # Baca column names dari cursor
        columns = [desc[0] for desc in cur.description]

        with open(output_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(columns)

            while True:
                rows = cur.fetchmany(fetch_size)
                if not rows:
                    break
                writer.writerows(rows)
                total_rows += len(rows)

                if total_rows % 50000 == 0:
                    elapsed = time.time() - start
                    print(f"  {total_rows} rows exported... ({elapsed:.1f}s)")

    conn.close()
    elapsed = time.time() - start
    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"✅ Streaming export: {total_rows} rows, {file_size_mb:.1f} MB")
    print(f"   Waktu: {elapsed:.1f}s ({total_rows/elapsed:.0f} rows/s)")


# ============================================
# METODE 3: Chunked Export (pecah jadi banyak file)
# ============================================
# Untuk data SANGAT besar, pecah jadi beberapa file
# Berguna untuk: paralel processing, upload ke cloud

def export_chunked(
    table_name: str,
    output_prefix: str,
    chunk_size: int = 100000,
    max_chunks: int = None
):
    """
    Export tabel besar dalam beberapa file CSV.
    Setiap file berisi chunk_size baris.

    Contoh: orders_001.csv, orders_002.csv, ...
    """
    print(f"\n{'='*50}")
    print(f"CHUNKED EXPORT: {table_name} -> {output_prefix}_*.csv")
    print(f"{'='*50}")

    conn = psycopg2.connect(**DB_CONFIG)
    start = time.time()
    total_rows = 0
    chunk_num = 0

    # Dapatkan total baris
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        total = cur.fetchone()[0]
        print(f"Total rows in table: {total}")

    if max_chunks:
        total = min(total, chunk_size * max_chunks)

    offset = 0
    while offset < total:
        chunk_num += 1
        output_path = f"{output_prefix}_{chunk_num:03d}.csv"

        query = f"""
            SELECT * FROM {table_name}
            ORDER BY order_id
            LIMIT {chunk_size} OFFSET {offset}
        """

        df = pd.read_sql(query, f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
        df.to_csv(output_path, index=False)

        offset += chunk_size
        total_rows += len(df)
        elapsed = time.time() - start
        print(f"  Chunk {chunk_num}: {output_path} ({len(df)} rows)")

    conn.close()
    elapsed = time.time() - start
    print(f"✅ Chunked export: {total_rows} rows in {chunk_num} files")
    print(f"   Waktu: {elapsed:.1f}s")


# ============================================
# METODE 4: Parallel Export (multi-thread)
# ============================================
# Export beberapa tabel ATAU partisi secara paralel

def _export_partition(
    query: str,
    output_path: str,
    partition_name: str
):
    """Export satu partisi (dipanggil oleh thread)."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        with conn.cursor(name=f"cur_{partition_name}") as cur:
            cur.execute(query)
            columns = [desc[0] for desc in cur.description]

            with open(output_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(columns)

                while True:
                    rows = cur.fetchmany(5000)
                    if not rows:
                        break
                    writer.writerows(rows)

        conn.close()
        size = os.path.getsize(output_path) / (1024 * 1024)
        print(f"  ✅ Thread {partition_name}: {output_path} ({size:.1f} MB)")
    except Exception as e:
        print(f"  ❌ Thread {partition_name} error: {e}")


def export_parallel(table_name: str, output_prefix: str, num_threads: int = 4):
    """
    Export tabel besar secara paralel dengan membagi data.
    Setiap thread export bagian data yang berbeda.
    """
    print(f"\n{'='*50}")
    print(f"PARALLEL EXPORT: {table_name} ({num_threads} threads)")
    print(f"{'='*50}")

    start = time.time()

    # Dapatkan range ID
    conn = psycopg2.connect(**DB_CONFIG)
    with conn.cursor() as cur:
        cur.execute(f"SELECT MIN(order_id), MAX(order_id) FROM {table_name}")
        min_id, max_id = cur.fetchone()
    conn.close()

    if not min_id or not max_id:
        print("❌ Tabel kosong")
        return

    # Bagi ID range per thread
    chunk_size = (max_id - min_id + 1) // num_threads
    threads = []

    for i in range(num_threads):
        start_id = min_id + (i * chunk_size)
        end_id = start_id + chunk_size - 1 if i < num_threads - 1 else max_id
        output_path = f"{output_prefix}_part{i+1}.csv"

        query = f"""
            SELECT * FROM {table_name}
            WHERE order_id BETWEEN {start_id} AND {end_id}
            ORDER BY order_id
        """

        thread = threading.Thread(
            target=_export_partition,
            args=(query, output_path, f"part{i+1}")
        )
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()

    elapsed = time.time() - start
    print(f"✅ Parallel export selesai dalam {elapsed:.1f}s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PostgreSQL to CSV Export")
    parser.add_argument("--table", default="ingestion.orders", help="Nama tabel")
    parser.add_argument("--query", help="SQL query kustom")
    parser.add_argument("--method", choices=["copy", "stream", "chunked", "parallel"], default="stream")
    parser.add_argument("--output", help="Path output file")
    parser.add_argument("--chunk-size", type=int, default=100000)
    parser.add_argument("--threads", type=int, default=4)
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    query = args.query or f"SELECT * FROM {args.table} ORDER BY order_id"
    output = args.output or os.path.join(OUTPUT_DIR, f"{args.table.replace('.', '_')}.csv")

    if args.method == "copy":
        export_copy_to(query, output)
    elif args.method == "stream":
        export_streaming(query, output)
    elif args.method == "chunked":
        export_chunked(args.table, output.replace(".csv", ""), args.chunk_size)
    elif args.method == "parallel":
        export_parallel(args.table, output.replace(".csv", ""), args.threads)
