import pandas as pd
from pymongo import MongoClient
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

# Make sure storage folder exists
os.makedirs("storage/exported", exist_ok=True)

# Export to Parquet
output_path = "storage/exported/flagged.parquet"
df.to_parquet(output_path, engine="pyarrow")

print(f"✅ Exported {len(df)} transactions to {output_path}")
