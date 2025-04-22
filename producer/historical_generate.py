import random
import pandas as pd
from uuid import uuid4
from datetime import datetime, timedelta, timezone
import os

# Output folder
BASE_DIR = "storage/historical"
os.makedirs(BASE_DIR, exist_ok=True)

# Simulation years
START_YEAR = 2000
END_YEAR = datetime.now(timezone.utc).year

# Config
USERS_PER_YEAR = 150  # start small, grows later
BASE_TRANSACTIONS = 3000  # base transactions per year
GROWTH_FACTOR = 1.4  # ~20% more txns per year
INFLATION_RATE = 0.025  # 2.5% inflation/year

# Static fields
CARD_TYPES = ["VISA", "MASTERCARD", "AMEX", "RUPAY"]
LOCATIONS = ["New York", "London", "Mumbai", "Tokyo", "Toronto", "Paris"]
MERCHANTS = ["groceries", "electronics", "travel", "crypto", "luxury", "fastfood"]
PAYMENT_METHODS = ["chip", "tap", "online", "swipe"]
STATUSES = ["success", "declined", "pending"]

def generate_yearly_transactions(year: int, user_pool: list, num_txns: int, inflation_multiplier: float):
    """
    Generates a list of fake transactions for a given year.

    Args:
        year (int): The target year to simulate.
        user_pool (list): List of user_ids.
        num_txns (int): Number of transactions to generate.
        inflation_multiplier (float): Adjusts amount based on inflation.

    Returns:
        list[dict]: List of transaction dicts.
    """
    start_date = datetime(year, 1, 1, tzinfo=timezone.utc)
    end_date = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
    delta = (end_date - start_date).total_seconds()

    transactions = []

    for _ in range(num_txns):
        txn_time = start_date + timedelta(seconds=random.randint(0, int(delta)))
        user_id = random.choice(user_pool)

        base_amount = random.uniform(10.0, 1000.0)
        amount = round(base_amount * inflation_multiplier, 2)

        txn = {
            "transaction_id": str(uuid4()),
            "timestamp": txn_time.isoformat(),
            "user_id": user_id,
            "amount": amount,
            "currency": "USD",
            "card_type": random.choice(CARD_TYPES),
            "location": random.choice(LOCATIONS),
            "ip_address": f"{random.randint(10, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}",
            "device_id": f"device_{random.randint(1000, 9999)}",
            "merchant_type": random.choice(MERCHANTS),
            "is_fraud": False,
            "geo_lat": round(random.uniform(-90, 90), 6),
            "geo_long": round(random.uniform(-180, 180), 6),
            "status": random.choices(STATUSES, weights=[0.9, 0.08, 0.02])[0],
            "payment_method": random.choice(PAYMENT_METHODS),
            "risk_score": round(random.uniform(0, 1), 3),
            "country": random.choice(["US", "UK", "IN", "JP", "FR", "CA"]),
        }

        transactions.append(txn)

    return transactions

print(f"📦 Generating historical transaction data from {START_YEAR} to {END_YEAR}...")

txn_count = 0

for year in range(START_YEAR, END_YEAR + 1):
    year_dir = os.path.join(BASE_DIR, str(year))
    os.makedirs(f"year={year_dir}", exist_ok=True)

    # Grow users and txns each year
    user_count = USERS_PER_YEAR + (year - START_YEAR) * 50  # 50 new users per year
    user_pool = [f"user_{year}_{i}" for i in range(user_count)]

    txns_this_year = int(BASE_TRANSACTIONS * (GROWTH_FACTOR ** (year - START_YEAR)))
    inflation_multiplier = (1 + INFLATION_RATE) ** (year - START_YEAR)

    print(f"📅 Year {year}: {len(user_pool)} users, {txns_this_year} transactions")

    # Generate data
    yearly_txns = generate_yearly_transactions(
        year=year,
        user_pool=user_pool,
        num_txns=txns_this_year,
        inflation_multiplier=inflation_multiplier,
    )

    # Save to Parquet
    df = pd.DataFrame(yearly_txns)
    output_path = os.path.join(year_dir, f"transactions-{year}.parquet")
    df.to_parquet(output_path, index=False)

    print(f"✅ Saved {len(df)} records to {output_path}\n")
    txn_count += len(df)

print(f"🎉 Done! Total generated transactions: {txn_count}")
