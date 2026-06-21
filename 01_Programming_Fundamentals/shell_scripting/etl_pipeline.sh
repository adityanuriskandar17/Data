#!/bin/bash
# ============================================
# SCRIPT ETL PIPELINE SEDERHANA
# ============================================
# ETL: Extract, Transform, Load menggunakan shell

set -euo pipefail  # strict mode: stop on error, undefined var, pipefail

# --- KONFIGURASI ---
SOURCE_DIR="/data/raw"
STAGING_DIR="/data/staging"
TARGET_DIR="/data/processed"
LOG_FILE="/var/log/etl_$(date +%Y%m%d_%H%M%S).log"

# --- FUNGSI LOGGING ---
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# --- EKSTRAKSI (EXTRACT) ---
extract() {
    log "Mulai ekstraksi data..."
    
    # Download dari SFTP
    sftp user@source-server:/data/orders_$(date +%Y%m%d).csv "$SOURCE_DIR/"
    
    # Copy dari S3 (contoh)
    # aws s3 cp s3://bucket/raw/orders.csv "$SOURCE_DIR/"
    
    # Ekstrak dari archive
    if [[ -f "$SOURCE_DIR/orders.csv.gz" ]]; then
        gunzip -f "$SOURCE_DIR/orders.csv.gz"
        log "File extracted: orders.csv"
    fi
    
    log "Ekstraksi selesai"
}

# --- TRANSFORMASI (TRANSFORM) ---
transform() {
    log "Mulai transformasi data..."
    
    mkdir -p "$STAGING_DIR"
    
    # Filter baris yang valid (bukan header, bukan baris kosong)
    awk -F',' 'NR>1 && NF>0 && $3!=""' "$SOURCE_DIR/orders.csv" > "$STAGING_DIR/orders_filtered.csv"
    
    # Konversi format tanggal
    sed -i 's|\([0-9]\{2\}\)/\([0-9]\{2\}\)/\([0-9]\{4\}\)|\3-\2-\1|g' "$STAGING_DIR/orders_filtered.csv"
    
    # Validasi data dengan awk
    awk -F',' '$2 > 0 {print $0}' "$STAGING_DIR/orders_filtered.csv" > "$STAGING_DIR/orders_valid.csv"
    
    row_count=$(wc -l < "$STAGING_DIR/orders_valid.csv")
    log "Transformasi selesai: $row_count baris valid"
}

# --- LOAD ---
load() {
    log "Mulai loading data..."
    
    mkdir -p "$TARGET_DIR"
    cp "$STAGING_DIR/orders_valid.csv" "$TARGET_DIR/orders_$(date +%Y%m%d).csv"
    
    # Load ke database (contoh dengan psql)
    # psql -h localhost -d warehouse -c "\copy staging_orders FROM '$STAGING_DIR/orders_valid.csv' CSV HEADER"
    
    # Buat file SUCCESS sebagai tanda pipeline selesai
    touch "$TARGET_DIR/_SUCCESS"
    
    log "Loading selesai"
}

# --- MAIN ---
main() {
    log "=== ETL Pipeline dimulai ==="
    extract
    transform
    load
    log "=== ETL Pipeline selesai ==="
}

main "$@"
