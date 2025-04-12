from faker import Faker
import uuid
import time
import random
from datetime import datetime, timezone

fake = Faker()

def generate_transaction():
    return {
        "transaction_id": str(uuid.uuid4()),
        "user_id": f"user_{random.randint(1, 1000)}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "amount": round(random.uniform(1.00, 1000.00), 2),
        "location": fake.city() + ", " + fake.country(),
        "merchant": fake.company(),
        "card_type": random.choice(["VISA", "MASTERCARD", "AMEX"])
    }

# while True:
#     txn = generate_transaction()
#     # print(txn)
#     time.sleep(1)
