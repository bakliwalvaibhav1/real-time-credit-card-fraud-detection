from kafka import KafkaProducer
import json
import time
from kafka.errors import KafkaError
from generate_transactions import generate_transaction

try:
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        retries=5
    )
except KafkaError as e:
    print(f"❌ Error creating producer: {e}")
    exit(1)

while True:
    txn = generate_transaction()
    future = producer.send('transactions', txn)

    try:
        record_metadata = future.get(timeout=10)
        print(f"✅ Sent: {txn}")
        print(f"📌 Metadata → topic: {record_metadata.topic}, partition: {record_metadata.partition}, offset: {record_metadata.offset}")
    except KafkaError as e:
        print(f"❌ Kafka error: {e}")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")

    time.sleep(0.2)
