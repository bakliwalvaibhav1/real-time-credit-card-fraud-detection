from kafka import KafkaConsumer
from pymongo import MongoClient
import json

# Set up MongoDB client
mongo_client = MongoClient("mongodb://localhost:27017")
db = mongo_client.frauddb
collection = db.transactions

# Set up Kafka consumer
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

        # Insert into MongoDB
        collection.insert_one(txn)
        print("✅ Inserted into MongoDB!\n")

    except json.JSONDecodeError:
        print(f"⚠️ Skipped malformed message: {raw}")
    except Exception as e:
        print(f"💥 Error inserting to MongoDB: {e}")
