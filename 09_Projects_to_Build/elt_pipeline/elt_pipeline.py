# ============================================
# PROYEK 1: ELT PIPELINE
# ============================================
# Extract dari API -> Load ke PostgreSQL -> Transform dengan SQL
# Bahasa Indonesia

import requests
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
import logging
import json

# Konfigurasi logging
logging.basicConfig(level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Konfigurasi database
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "warehouse",
    "user": "de_user",
    "password": "de_password"
}
DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

API_URL = "https://jsonplaceholder.typicode.com/posts"  # Contoh API gratis


# =====================
# 1. EXTRACT
# =====================
def extract_from_api(api_url: str, params: dict = None) -> pd.DataFrame:
    """Mengambil data dari REST API."""
    logger.info(f"Extract data dari {api_url}")

    response = requests.get(api_url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame(data)
    df["_extracted_at"] = datetime.now()

    logger.info(f"Berhasil extract {len(df)} baris")
    return df


def extract_from_csv(file_path: str) -> pd.DataFrame:
    """Alternatif: extract dari file CSV."""
    logger.info(f"Extract data dari {file_path}")
    df = pd.read_csv(file_path)
    df["_extracted_at"] = datetime.now()
    return df


# =====================
# 2. LOAD (ke staging)
# =====================
def load_to_staging(df: pd.DataFrame, engine, table_name: str = "staging_posts"):
    """Load data mentah ke tabel staging di database."""
    logger.info(f"Load {len(df)} baris ke tabel {table_name}")

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False,
        method="multi"
    )

    # Verifikasi
    with engine.connect() as conn:
        count = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
        logger.info(f"Verifikasi: {count} baris di tabel {table_name}")


# =====================
# 3. TRANSFORM (di database)
# =====================
def transform_in_db(engine):
    """Transformasi data menggunakan SQL langsung di database."""
    logger.info("Mulai transformasi data di database...")

    with engine.connect() as conn:
        # Buat schema jika belum ada
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS silver;"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS gold;"))

        # Silver layer: data bersih
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS silver.posts AS
            SELECT
                id AS post_id,
                userId AS user_id,
                title,
                body,
                _extracted_at
            FROM staging_posts
            WHERE title IS NOT NULL AND body IS NOT NULL;
        """))

        # Gold layer: agregasi
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS gold.post_summary AS
            SELECT
                user_id,
                COUNT(*) AS total_posts,
                AVG(LENGTH(title)) AS avg_title_length,
                AVG(LENGTH(body)) AS avg_body_length
            FROM silver.posts
            GROUP BY user_id;
        """))

        conn.commit()

    logger.info("Transformasi selesai!")


# =====================
# MAIN PIPELINE
# =====================
def run_elt_pipeline():
    """Menjalankan pipeline ELT end-to-end."""
    start_time = datetime.now()
    logger.info("=== ELT Pipeline dimulai ===")

    try:
        # Koneksi ke database
        engine = create_engine(DATABASE_URL)

        # Extract
        df = extract_from_api(API_URL)

        # Load
        load_to_staging(df, engine)

        # Transform
        transform_in_db(engine)

        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"=== ELT Pipeline selesai dalam {duration:.2f} detik ===")

    except Exception as e:
        logger.error(f"Pipeline gagal: {str(e)}")
        raise


if __name__ == "__main__":
    run_elt_pipeline()
