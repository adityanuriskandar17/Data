# ============================================
# DATABASE — SQLite (default) / PostgreSQL
# ============================================
#
# 🔹 DEFAULT: SQLite (tanpa setup, file lokal)
# 🔹 Untuk PostgreSQL, set env variable:
#    export DB_HOST=localhost
#    export DB_PORT=5432
#    export DB_USER=postgres
#    export DB_PASSWORD=your_password
#    export DB_NAME=de_learning
#    export USE_PG=1

import os
import databases
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, DateTime, text
from sqlalchemy.sql import select
from datetime import datetime

SQLITE_PATH = os.path.join(os.path.dirname(__file__), "..", "de_learning.db")
SQLITE_URL = f"sqlite:///{SQLITE_PATH}"

USE_PG = os.getenv("USE_PG", "1") == "1"

if USE_PG:
    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "user": os.getenv("DB_USER", "bosani"),
        "password": os.getenv("DB_PASSWORD", "1234567890"),
        "database": os.getenv("DB_NAME", "latihan_de"),
    }
    DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
else:
    DATABASE_URL = SQLITE_URL

database = databases.Database(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
metadata = MetaData()

# --- TABEL PROGRESS ---
progress_table = Table(
    "progress",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("file_path", String(500), unique=True, nullable=False),
    Column("completed", Boolean, default=False),
    Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
)


async def _connect_db(url: str):
    """Try to connect and create tables."""
    global DATABASE_URL, database, engine
    DATABASE_URL = url
    engine = create_engine(url, connect_args={"check_same_thread": False} if "sqlite" in url else {})
    if "sqlite" in url:
        with engine.connect() as conn:
            conn.execute(text("PRAGMA journal_mode=WAL;"))
    metadata.create_all(engine)
    database = databases.Database(url)
    await database.connect()


async def init_db():
    """Init database and create tables."""
    try:
        await _connect_db(DATABASE_URL)
        db_type = "SQLite" if "sqlite" in DATABASE_URL else "PostgreSQL"
        print(f"✅ Database OK: {db_type}")
    except Exception as e:
        print(f"❌ Database error: {e}")
        if USE_PG:
            print("⚠️  PostgreSQL gagal. Fallback ke SQLite...")
            try:
                await _connect_db(SQLITE_URL)
                print(f"✅ Database OK (SQLite fallback)")
            except Exception as e2:
                print(f"❌ SQLite juga gagal: {e2}")


async def get_all_progress():
    """Get all progress records."""
    query = select(progress_table)
    rows = await database.fetch_all(query)
    return [dict(row) for row in rows]


async def toggle_progress(file_path: str):
    """Toggle progress for a file."""
    query = select(progress_table).where(progress_table.c.file_path == file_path)
    row = await database.fetch_one(query)

    if row:
        new_status = not row["completed"]
        update = (
            progress_table.update()
            .where(progress_table.c.file_path == file_path)
            .values(completed=new_status, updated_at=datetime.utcnow())
        )
        await database.execute(update)
        return {"file_path": file_path, "completed": new_status}
    else:
        insert = progress_table.insert().values(
            file_path=file_path,
            completed=True,
            updated_at=datetime.utcnow()
        )
        await database.execute(insert)
        return {"file_path": file_path, "completed": True}


def get_db_session():
    return database
