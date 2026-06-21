# ============================================
# FULL INGESTION ORCHESTRATOR
# ============================================
# Pipeline lengkap: Generate → Load → Transfer → Export
# Meniru alur data engineering di production

import subprocess
import sys
import os
import time
from datetime import datetime

PYTHON = sys.executable
BASE_DIR = os.path.dirname(__file__)


def run_step(step_name: str, script: str, args: list = None):
    """Jalankan satu step dalam pipeline."""
    print(f"\n{'='*60}")
    print(f"  STEP: {step_name}")
    print(f"  Script: {script}")
    print(f"{'='*60}")

    cmd = [PYTHON, os.path.join(BASE_DIR, script)]
    if args:
        cmd.extend(args)

    start = time.time()
    result = subprocess.run(cmd, capture_output=False)

    elapsed = time.time() - start
    status = "✅" if result.returncode == 0 else "❌"
    print(f"{status} Step '{step_name}' selesai dalam {elapsed:.1f}s\n")

    if result.returncode != 0:
        print(f"ERROR: {result.stderr.decode() if result.stderr else 'Unknown'}")
        sys.exit(1)

    return result


def main():
    """Jalankan full ingestion pipeline."""
    print(f"\n{'='*60}")
    print(f"  DATA INGESTION PIPELINE")
    print(f"  Started at: {datetime.now().isoformat()}")
    print(f"{'='*60}\n")

    start_total = time.time()

    # Step 1: Generate data
    run_step("Generate Sample Data", "data/generate_data.py", [
        "--customers", "100000",
        "--orders", "500000"
    ])

    # Step 2: Setup tabel di PostgreSQL
    run_step("Setup Tables", None)  # via SQL langsung
    # Alternatif: jalankan setup_tables.sql
    subprocess.run([
        "psql", "-h", "localhost", "-U", "bosani", "-d", "latihan_de",
        "-f", os.path.join(BASE_DIR, "setup_tables.sql")
    ], check=True)
    print("✅ Setup tables selesai\n")

    # Step 3: CSV → PostgreSQL (ingestion.orders)
    run_step("CSV to PostgreSQL", "csv_to_postgres.py", [
        os.path.join(BASE_DIR, "data", "orders.csv"),
        "--table", "ingestion.orders",
        "--method", "copy"
    ])

    # Step 4: CSV → PostgreSQL (ingestion.customers)
    run_step("CSV to PostgreSQL (customers)", "csv_to_postgres.py", [
        os.path.join(BASE_DIR, "data", "customers.csv"),
        "--table", "ingestion.customers",
        "--method", "copy"
    ])

    # Step 5: CSV → PostgreSQL (ingestion.products)
    run_step("CSV to PostgreSQL (products)", "csv_to_postgres.py", [
        os.path.join(BASE_DIR, "data", "products.csv"),
        "--table", "ingestion.products",
        "--method", "copy"
    ])

    # Step 6: Database A → Database B (transfer + agregasi)
    run_step("Transfer + Aggregate (DB to DB)", "db_to_db.py", [
        "--method", "agg"
    ])

    # Step 7: PostgreSQL → CSV (export)
    run_step("Export to CSV", "postgres_to_csv.py", [
        "--table", "ingestion_dest.orders_summary",
        "--method", "stream",
        "--output", os.path.join(BASE_DIR, "exports", "orders_summary.csv")
    ])

    # Step 8: Large data handling demo
    run_step("Large DB Handling (batch)", "large_db_handling.py", [
        "--example", "batch"
    ])

    elapsed_total = time.time() - start_total
    print(f"\n{'='*60}")
    print(f"  ✅ PIPELINE COMPLETE")
    print(f"  Total time: {elapsed_total:.1f}s")
    print(f"  Finished at: {datetime.now().isoformat()}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
