import streamlit as st
from streamlit_autorefresh import st_autorefresh
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
st.divider()
st.subheader("📈 Fraud Analytics")

# Auto-refresh every 30 seconds
st_autorefresh(interval=30_000, key="data_refresh")

# Load flagged transactions
data = list(flagged_txns.find())

if not data:
    st.warning("No flagged transactions found.")
else:
    for txn in data:
        txn.pop("_id", None)
    df = pd.DataFrame(data)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # --- Charts ---

    # Line chart: amount over time
    time_series = (
        df.groupby(pd.Grouper(key="timestamp", freq="1min"))["amount"]
        .sum()
        .reset_index()
    )
    st.line_chart(time_series.rename(columns={"timestamp": "index"}).set_index("index"))

    # Bar chart: top fraud users
    top_users = df["user_id"].value_counts().head(10)
    st.bar_chart(top_users)

    # --- Table ---

    st.divider()
    st.subheader("🧾 Recent Flagged Transactions")

    df_sorted = df.sort_values(by="timestamp", ascending=False)
    columns_to_show = ["timestamp", "user_id", "amount", "card_type", "location"]
    for col in columns_to_show:
        if col not in df_sorted.columns:
            df_sorted[col] = "N/A"

    st.dataframe(df_sorted[columns_to_show].head(50), use_container_width=True)

