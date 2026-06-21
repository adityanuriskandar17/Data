#!/bin/bash
# ============================================
# SHELL SCRIPTING UNTUK DATA ENGINEERING
# ============================================
# Bahasa Indonesia

echo "=== Shell Scripting untuk Data Engineer ==="

# --- VARIABEL ---
DB_HOST="localhost"
DB_PORT=5432
DB_NAME="data_warehouse"
BACKUP_DIR="/backup/$(date +%Y%m%d)"
echo "Backup directory: $BACKUP_DIR"

# --- INPUT ARGUMENTS ---
MODE=${1:-"daily"}  # default: daily
echo "Mode: $MODE"

# --- CONDITIONAL ---
if [ -d "$BACKUP_DIR" ]; then
    echo "Directory sudah ada"
else
    mkdir -p "$BACKUP_DIR"
    echo "Directory dibuat: $BACKUP_DIR"
fi

# --- LOOPING ---
for table in customers orders products; do
    echo "Memproses table: $table"
    pg_dump -h $DB_HOST -p $DB_PORT -d $DB_NAME -t $table > "$BACKUP_DIR/${table}.sql"
done

# --- FUNCTION ---
send_notification() {
    local message=$1
    local webhook_url="https://hooks.slack.com/services/xxx"
    curl -X POST -H "Content-Type: application/json" \
         -d "{\"text\": \"$message\"}" \
         "$webhook_url"
}

# --- CHECK EXIT CODE ---
if pg_dump -h $DB_HOST $DB_NAME > dump.sql; then
    echo "Backup sukses"
else
    echo "Backup gagal!" >&2
    send_notification "Backup gagal untuk $DB_NAME"
    exit 1
fi

# --- CRON JOB (contoh) ---
# Jalankan setiap jam 2 pagi:
# 0 2 * * * /home/user/scripts/backup.sh >> /var/log/backup.log 2>&1
