from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.frauddb
print("✅ Connected to MongoDB!")
print("Collections:", db.list_collection_names())
