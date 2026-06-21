# ============================================
# RUN WEB APP
# ============================================
# Kamu bisa atur environment variable berikut:
# DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
# Atau set USE_SQLITE=1 untuk pakai SQLite

from backend.app import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
