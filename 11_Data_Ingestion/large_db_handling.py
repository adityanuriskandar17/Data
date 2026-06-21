# ============================================
# LARGE DATABASE HANDLING
# ============================================
# Teknik-teknik untuk menangani data SANGAT BESAR
# (ratusan GB hingga TB)
#
# Topik:
# 1. Chunking — pecah data jadi potongan kecil
# 2. Batch processing — proses per batch
# 3. Parallel processing — proses simultan
# 4. Memory management — hindari OOM (Out of Memory)
# 5. Progress tracking — tahu progress untuk data besar

import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
import time
import os
import argparse
import threading
from queue import Queue
from datetime import datetime

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "user": os.getenv("DB_USER", "bosani"),
    "password": os.getenv("DB_PASSWORD", "1234567890"),
    "database": os.getenv("DB_NAME", "latihan_de"),
}


# ============================================
# 1. CHUNKED READ — Baca data dalam potongan
# ============================================
# Hindari OOM dengan membaca data dalam batch kecil

def chunked_read_sql(
    query_template: str,
    id_column: str,
    min_id: int,
    max_id: int,
    chunk_size: int = 50000
):
    """
    Baca tabel besar dalam chunk berdasarkan range ID.
    Cocok untuk tabel dengan ID berurutan.
    
    Args:
        query_template: query dengan placeholder {start} dan {end}
        id_column: nama kolom ID
        min_id: ID minimum
        max_id: ID maksimum
        chunk_size: jumlah baris per chunk
    
    Yields:
        DataFrame per chunk (tidak pernah full table di memory)
    """
    conn = psycopg2.connect(**DB_CONFIG)
    start_time = time.time()
    total = 0
    current = min_id

    while current <= max_id:
        end = min(current + chunk_size - 1, max_id)
        query = query_template.format(start=current, end=end)

        df = pd.read_sql(query, conn)
        if len(df) == 0:
            current = end + 1
            continue

        total += len(df)
        yield df

        current = end + 1

    conn.close()
    print(f"  Total: {total} rows from {min_id} to {max_id}")


# Contoh penggunaan chunked read
def example_chunked_read():
    """Contoh: baca semua orders dalam chunk."""
    print("\n=== CHUNKED READ EXAMPLE ===")

    conn = psycopg2.connect(**DB_CONFIG)
    with conn.cursor() as cur:
        cur.execute("SELECT MIN(order_id), MAX(order_id) FROM ingestion.orders")
        min_id, max_id = cur.fetchone()
    conn.close()

    for i, chunk in enumerate(chunked_read_sql(
        "SELECT * FROM ingestion.orders WHERE order_id BETWEEN {start} AND {end}",
        "order_id", min_id, max_id, chunk_size=50000
    )):
        print(f"  Chunk {i+1}: {len(chunk)} rows, {chunk['total_amount'].sum():,.0f} total")


# ============================================
# 2. BATCH PROCESSING — Insert/PROSES dalam batch
# ============================================

def batch_insert_from_query(
    source_query: str,
    target_table: str,
    batch_size: int = 5000
):
    """
    Baca data dan insert ke tabel lain dalam batch.
    Tidak pernah menyimpan semua data di memory.
    """
    print(f"\n=== BATCH PROCESSING ===")
    print(f"  Source query -> {target_table}")

    src_conn = psycopg2.connect(**DB_CONFIG)
    tgt_conn = psycopg2.connect(**DB_CONFIG)
    start = time.time()
    total_rows = 0

    with src_conn.cursor(name="batch_cursor") as src_cur:
        src_cur.execute(source_query)
        columns = [desc[0] for desc in src_cur.description]
        col_names = ", ".join(columns)

        while True:
            rows = src_cur.fetchmany(batch_size)
            if not rows:
                break

            with tgt_conn.cursor() as tgt_cur:
                execute_values(
                    tgt_cur,
                    f"INSERT INTO {target_table} ({col_names}) VALUES %s ON CONFLICT DO NOTHING",
                    rows,
                    page_size=batch_size
                )
            tgt_conn.commit()

            total_rows += len(rows)
            elapsed = time.time() - start
            rate = total_rows / elapsed if elapsed > 0 else 0
            print(f"  Batch: {total_rows} rows | {elapsed:.1f}s | {rate:.0f} rows/s")

    src_conn.close()
    tgt_conn.close()
    print(f"✅ Batch processing: {total_rows} rows in {elapsed:.1f}s")


# ============================================
# 3. PARALLEL PROCESSING — Multi-thread processing
# ============================================

class ParallelProcessor:
    """
    Proses data secara paralel dengan worker threads.
    
    Cara kerja:
    1. Range data dibagi per thread
    2. Setiap thread memproses bagiannya sendiri
    3. Hasil digabungkan (atau ditulis ke tujuan masing-masing)
    """

    def __init__(self, num_workers: int = 4):
        self.num_workers = num_workers

    def process_table(
        self,
        table_name: str,
        id_column: str,
        process_fn,
        min_id: int = None,
        max_id: int = None
    ):
        """Proses tabel secara paralel."""
        if not min_id or not max_id:
            conn = psycopg2.connect(**DB_CONFIG)
            with conn.cursor() as cur:
                cur.execute(f"SELECT MIN({id_column}), MAX({id_column}) FROM {table_name}")
                min_id, max_id = cur.fetchone()
            conn.close()

        chunk_size = (max_id - min_id + 1) // self.num_workers
        threads = []
        results = Queue()

        for i in range(self.num_workers):
            start_id = min_id + (i * chunk_size)
            end_id = start_id + chunk_size - 1 if i < self.num_workers - 1 else max_id

            thread = threading.Thread(
                target=self._worker,
                args=(process_fn, table_name, id_column, start_id, end_id, results, i + 1)
            )
            threads.append(thread)
            thread.start()

        for t in threads:
            t.join()

        # Kumpulkan hasil
        total_rows = 0
        while not results.empty():
            total_rows += results.get()

        return total_rows

    def _worker(self, process_fn, table_name, id_column, start_id, end_id, results, worker_id):
        """Worker thread."""
        print(f"  Worker {worker_id}: processing IDs {start_id}..{end_id}")
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            query = f"SELECT * FROM {table_name} WHERE {id_column} BETWEEN {start_id} AND {end_id}"
            df = pd.read_sql(query, conn)
            conn.close()

            # Proses data
            result = process_fn(df, worker_id)
            results.put(len(df))
            print(f"  ✅ Worker {worker_id}: {len(df)} rows done")
        except Exception as e:
            print(f"  ❌ Worker {worker_id}: {e}")
            results.put(0)


def example_parallel_processing():
    """Contoh: hitung total revenue per worker secara paralel."""
    def hitung_revenue(df: pd.DataFrame, worker_id: int) -> int:
        """Hitung total revenue untuk satu partisi data."""
        total = df["total_amount"].sum()
        print(f"    Worker {worker_id}: revenue = Rp{total:,.0f}")
        return len(df)

    print("\n=== PARALLEL PROCESSING EXAMPLE ===")
    processor = ParallelProcessor(num_workers=4)
    total = processor.process_table(
        table_name="ingestion.orders",
        id_column="order_id",
        process_fn=hitung_revenue
    )
    print(f"✅ Total rows processed: {total}")


# ============================================
# 4. MEMORY MANAGEMENT
# ============================================

def check_memory_usage():
    """Cek penggunaan memory sebelum dan sesudah operasi."""
    import psutil
    process = psutil.Process(os.getpid())
    mem = process.memory_info()
    print(f"  RSS: {mem.rss / 1024 / 1024:.1f} MB")
    print(f"  VMS: {mem.vms / 1024 / 1024:.1f} MB")


# ============================================
# 5. PROGRESS TRACKING
# ============================================

class ProgressTracker:
    """Tracking progress untuk operasi large data."""

    def __init__(self, total_expected: int, description: str = "Processing"):
        self.total_expected = total_expected
        self.description = description
        self.processed = 0
        self.start_time = time.time()
        self._last_print = 0

    def update(self, n: int):
        """Update progress dengan n baris yang sudah diproses."""
        self.processed += n
        now = time.time()

        # Print setiap 5 detik
        if now - self._last_print > 5:
            pct = (self.processed / self.total_expected) * 100
            elapsed = now - self.start_time
            rate = self.processed / elapsed if elapsed > 0 else 0
            eta = (self.total_expected - self.processed) / rate if rate > 0 else 0

            print(f"  {self.description}: {self.processed:,}/{self.total_expected:,} "
                  f"({pct:.1f}%) | "
                  f"{rate:.0f} rows/s | "
                  f"ETA: {eta:.0f}s")
            self._last_print = now

    def done(self):
        elapsed = time.time() - self.start_time
        print(f"✅ {self.description} selesai: {self.processed:,} rows in {elapsed:.1f}s")


def example_progress_tracking():
    """Contoh penggunaan ProgressTracker."""
    print("\n=== PROGRESS TRACKING EXAMPLE ===")

    conn = psycopg2.connect(**DB_CONFIG)
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM ingestion.orders")
        total = cur.fetchone()[0]
    conn.close()

    tracker = ProgressTracker(total, "Processing orders")
    chunk_size = 10000

    for i, chunk in enumerate(pd.read_sql(
        "SELECT * FROM ingestion.orders ORDER BY order_id",
        conn,
        chunksize=chunk_size
    )):
        # Simulasi processing
        time.sleep(0.1)  # ganti dengan proses beneran
        tracker.update(len(chunk))

    tracker.done()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--example", choices=["chunked", "batch", "parallel", "progress"], default="batch")
    args = parser.parse_args()

    if args.example == "chunked":
        example_chunked_read()
    elif args.example == "batch":
        batch_insert_from_query(
            "SELECT * FROM ingestion.orders WHERE status IN ('pending', 'confirmed')",
            "ingestion.orders_backup"
        )
    elif args.example == "parallel":
        example_parallel_processing()
    elif args.example == "progress":
        example_progress_tracking()
