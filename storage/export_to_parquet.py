import pandas as pd
from pymongo import MongoClient
from datetime import datetime, timezone
import os

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client.frauddb
collection = db.flagged_transactions

# Fetch all flagged transactions
transactions = list(collection.find())

if not transactions:
    print("⚠️ No flagged transactions found.")
    exit()

# Remove MongoDB ObjectId field
for txn in transactions:
    txn.pop('_id', None)

# Convert to DataFrame
df = pd.DataFrame(transactions)

# Timestamp-based folder
now = datetime.now(timezone.utc)
day = now.strftime("%Y-%m-%d")
hour = now.strftime("hour=%H")
output_dir = f"storage/exported/{day}/{hour}"
os.makedirs(output_dir, exist_ok=True)

# Filename with timestamp to avoid collisions
filename = f"flagged-{now.strftime('%Y%m%d-%H%M%S')}.parquet"
output_path = os.path.join(output_dir, filename)

# Write the file
df.to_parquet(output_path, engine="pyarrow")
print(f"✅ Exported {len(df)} transactions to {output_path}")
