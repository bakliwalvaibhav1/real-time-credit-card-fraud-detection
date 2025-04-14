from kafka import KafkaConsumer
from pymongo import MongoClient
from collections import defaultdict, deque
from datetime import datetime, timedelta
import json

# MongoDB setup
mongo_client = MongoClient("mongodb://localhost:27017")
db = mongo_client.frauddb
collection_all = db.transactions
collection_flagged = db.flagged_transactions

# Kafka setup
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='fraud-detector-group',
    value_deserializer=lambda x: x.decode('utf-8')
)

print("⏳ Waiting for transactions...\n")

# In-memory tracker for high-frequency detection
recent_txns = defaultdict(lambda: deque(maxlen=10))  # store last few timestamps per user

last_locations = {}

def is_suspicious(txn: dict) -> bool:
    txn_time = datetime.fromisoformat(txn["timestamp"])

    # High Amount Rule
    if txn["amount"] > 900:
        return True

    # Rule 2: High Frequency (same as before)
    user_id = txn["user_id"]
    recent = recent_txns[user_id]
    recent = deque([t for t in recent if (txn_time - t).total_seconds() <= 10])
    recent.append(txn_time)
    recent_txns[user_id] = recent
    if len(recent) >= 3:
        return True

    # Rule 3: Unusual Hour
    hour = txn_time.hour
    if 0 <= hour < 5:
        return True

    # ✅ Geo Mismatch Rule
    user = txn["user_id"]
    loc = txn.get("location")

    if user in last_locations:
        if last_locations[user] != loc:
            return True  # location mismatch
    last_locations[user] = loc

    return False

for message in consumer:
    raw = message.value
    try:
        txn = json.loads(raw)
        print(f"🔍 Received: {txn}")

        collection_all.insert_one(txn)
        print("✅ Inserted into MongoDB (all)\n")

        if is_suspicious(txn):
            collection_flagged.insert_one(txn)
            print("🚨 Fraud Detected! Inserted into flagged collection\n")

    except json.JSONDecodeError:
        print(f"⚠️ Skipped malformed message: {raw}")
    except Exception as e:
        print(f"💥 Error inserting to MongoDB: {e}")
