from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='fraud-detector-group',
    value_deserializer=lambda x: x.decode('utf-8')
)

print("⏳ Waiting for transactions...\n")

for message in consumer:
    raw = message.value
    try:
        txn = json.loads(raw)
        print(f"🔍 Received: {txn}")
    except json.JSONDecodeError:
        print(f"⚠️ Skipped malformed message: {raw}")
