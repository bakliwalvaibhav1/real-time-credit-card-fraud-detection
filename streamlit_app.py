import streamlit as st
import pandas as pd
from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb://localhost:27017")
db = client.frauddb
all_txns = db.transactions
flagged_txns = db.flagged_transactions

# Layout
st.set_page_config(page_title="Fraud Detection Dashboard", layout="wide")
st.title("🛡️ Real-Time Fraud Detection Dashboard")

# Stats
col1, col2 = st.columns(2)
# col1.metric("🔁 Total Transactions", all_txns.count_documents({}))
# col2.metric("🚨 Flagged as Fraud", flagged_txns.count_documents({}))
st.divider()
st.subheader("📈 Fraud Analytics")

# Load flagged transactions into a DataFrame
data = list(flagged_txns.find())
if not data:
    st.warning("No flagged transactions found.")
else:
    for txn in data:
        txn.pop("_id", None)  # remove MongoDB ObjectId for clean DataFrame

    df = pd.DataFrame(data)

    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Line Chart: Fraud Amount Over Time
    time_series = (
        df.groupby(pd.Grouper(key="timestamp", freq="1min"))["amount"]
        .sum()
        .reset_index()
    )
    st.line_chart(time_series.rename(columns={"timestamp": "index"}).set_index("index"))

    # Bar Chart: Top Fraudster Users
    top_users = df["user_id"].value_counts().head(10)
    st.bar_chart(top_users)

