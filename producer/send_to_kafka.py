from kafka import KafkaProducer
import json
import time
from generate_transactions import generate_transaction

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    txn = generate_transaction()
    producer.send('transactions', txn)
    print(f"Sent: {txn}")
    time.sleep(1)
