# ============================================
# GENERATE SAMPLE DATASET
# ============================================
# Membuat CSV realistis untuk latihan data ingestion
# Bisa generate jutaan baris untuk simulasi large data

import csv
import random
import uuid
from datetime import datetime, timedelta
import os
import argparse
import time

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data")

PRODUCTS = [
    ("P001", "Laptop ThinkPad X1", "Elektronik", 15000000),
    ("P002", "Mouse Wireless", "Elektronik", 250000),
    ("P003", "Keyboard Mechanical", "Elektronik", 750000),
    ("P004", "Monitor 27 inch", "Elektronik", 3500000),
    ("P005", "Headset Bluetooth", "Elektronik", 500000),
    ("P006", "Buku Python Programming", "Buku", 150000),
    ("P007", "Buku Data Engineering", "Buku", 200000),
    ("P008", "Meja Standing Desk", "Furniture", 2500000),
    ("P009", "Kursi Ergonomis", "Furniture", 3500000),
    ("P010", "Lampu Meja LED", "Furniture", 350000),
    ("P011", "SSD 1TB External", "Elektronik", 1800000),
    ("P012", "Webcam 4K", "Elektronik", 1200000),
    ("P013", "Microphone USB", "Elektronik", 850000),
    ("P014", "USB-C Hub 7in1", "Elektronik", 450000),
    ("P015", "Mousepad Large", "Aksesoris", 150000),
]

CITIES = [
    "Jakarta", "Bandung", "Surabaya", "Medan", "Yogyakarta",
    "Semarang", "Makassar", "Palembang", "Denpasar", "Balikpapan"
]

STATUSES = ["pending", "confirmed", "shipped", "delivered", "cancelled"]
PROVINCES = {
    "Jakarta": "DKI Jakarta", "Bandung": "Jawa Barat",
    "Surabaya": "Jawa Timur", "Medan": "Sumatera Utara",
    "Yogyakarta": "DI Yogyakarta", "Semarang": "Jawa Tengah",
    "Makassar": "Sulawesi Selatan", "Palembang": "Sumatera Selatan",
    "Denpasar": "Bali", "Balikpapan": "Kalimantan Timur"
}


def generate_customers(n: int, filename: str = "customers.csv"):
    """Generate sample customer data."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    print(f"Generating {n} customers -> {filepath}")
    start = time.time()

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["customer_id", "name", "email", "city", "province", "phone", "created_at"])

        for i in range(1, n + 1):
            city = random.choice(CITIES)
            name = f"Customer_{i:06d}"
            email = f"customer{i}@email.com"
            phone = f"08{random.randint(100000000, 999999999)}"
            created = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 730))
            writer.writerow([i, name, email, city, PROVINCES[city], phone, created.date()])

            if i % 100000 == 0:
                print(f"  Progress: {i}/{n} customers")

    elapsed = time.time() - start
    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    print(f"  Done: {n} customers in {elapsed:.1f}s, {size_mb:.1f} MB")


def generate_orders(n: int, max_customer_id: int, filename: str = "orders.csv"):
    """Generate sample order data."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    print(f"Generating {n} orders -> {filepath}")
    start = time.time()

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "order_id", "customer_id", "product_id", "product_name",
            "category", "qty", "unit_price", "total_amount",
            "order_date", "status", "city", "province"
        ])

        for i in range(1, n + 1):
            cust_id = random.randint(1, max_customer_id)
            prod = random.choice(PRODUCTS)
            qty = random.randint(1, 5)
            city = random.choice(CITIES)
            order_date = datetime(2024, 1, 1) + timedelta(
                days=random.randint(0, 365),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            status = random.choices(STATUSES, weights=[5, 15, 20, 50, 10])[0]

            writer.writerow([
                i, cust_id, prod[0], prod[1], prod[2],
                qty, prod[3], prod[3] * qty,
                order_date.strftime("%Y-%m-%d %H:%M:%S"),
                status, city, PROVINCES[city]
            ])

            if i % 100000 == 0:
                print(f"  Progress: {i}/{n} orders")

    elapsed = time.time() - start
    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    print(f"  Done: {n} orders in {elapsed:.1f}s, {size_mb:.1f} MB")


def generate_products(filename: str = "products.csv"):
    """Generate product data (small, static)."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    print(f"Generating products -> {filepath}")

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["product_id", "product_name", "category", "unit_price", "stock"])
        for p in PRODUCTS:
            writer.writerow([p[0], p[1], p[2], p[3], random.randint(10, 500)])

    size_kb = os.path.getsize(filepath) / 1024
    print(f"  Done: {len(PRODUCTS)} products, {size_kb:.1f} KB")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--customers", type=int, default=100000, help="Jumlah customers")
    parser.add_argument("--orders", type=int, default=500000, help="Jumlah orders")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Dataset: {args.customers} customers, {args.orders} orders\n")

    generate_products()
    generate_customers(args.customers)
    generate_orders(args.orders, args.customers)

    print("\n✅ Semua dataset siap!")
    print(f"  ls -lh {OUTPUT_DIR}/")
