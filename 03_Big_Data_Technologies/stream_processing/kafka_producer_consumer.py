# ============================================
# APACHE KAFKA UNTUK STREAM PROCESSING
# ============================================
# Bahasa Indonesia

from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
import json
import time
import random

# =====================
# ADMIN: Membuat Topik
# =====================
admin = KafkaAdminClient(bootstrap_servers="localhost:9092")
topic = NewTopic(name="orders", num_partitions=3, replication_factor=1)
admin.create_topics([topic])

# =====================
# PRODUCER: Mengirim Data
# =====================
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: str(k).encode("utf-8")
)

def send_order(order_data: dict):
    future = producer.send(
        topic="orders",
        key=order_data["order_id"],
        value=order_data
    )
    result = future.get(timeout=10)
    print(f"Sent order {order_data['order_id']} to partition {result.partition}")
    return result

# Simulasi pengiriman data order
for i in range(100):
    order = {
        "order_id": i,
        "customer_id": random.randint(1, 1000),
        "product": random.choice(["laptop", "phone", "tablet"]),
        "amount": round(random.uniform(100, 5000), 2),
        "timestamp": int(time.time() * 1000)
    }
    send_order(order)
    time.sleep(0.1)

producer.flush()

# =====================
# CONSUMER: Membaca Data
# =====================
consumer = KafkaConsumer(
    "orders",
    bootstrap_servers="localhost:9092",
    group_id="etl-group",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    key_deserializer=lambda k: int(k.decode("utf-8"))
)

for message in consumer:
    print(f"""
    Partition: {message.partition}
    Offset: {message.offset}
    Key: {message.key}
    Value: {message.value}
    """)
    # Proses data di sini
    if message.value["amount"] > 1000:
        print(f"  -> High value order detected!")

# =====================
# PRODUCER DENGAN KEY
# =====================
# Menggunakan key agar order customer yang sama masuk ke partition yang sama
# Ini penting untuk menjamin ordering per customer
