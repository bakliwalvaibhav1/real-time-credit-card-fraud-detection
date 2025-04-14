import streamlit as st
import pandas as pd
from pymongo import MongoClient
import io

# MongoDB setup
client = MongoClient("mongodb://localhost:27017")
db = client.frauddb
all_txns = db.transactions
flagged_txns = db.flagged_transactions

# Layout
st.set_page_config(page_title="Fraud Detection Dashboard", layout="wide")
st.title("🛡️ Real-Time Fraud Detection Dashboard")

# Load flagged transactions
data = list(flagged_txns.find())
for txn in data:
    txn.pop("_id", None)

df = pd.DataFrame(data)

if df.empty:
    st.warning("⚠️ No flagged transactions found.")
else:
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # --- SIDEBAR FILTERS ---
    st.sidebar.header("🔎 Filters")

    # Amount range
    min_amt, max_amt = st.sidebar.slider(
        "Amount Range",
        min_value=float(df["amount"].min()),
        max_value=float(df["amount"].max()),
        value=(float(df["amount"].min()), float(df["amount"].max()))
    )

    # Card type multiselect
    card_types = st.sidebar.multiselect(
        "Card Type",
        options=df["card_type"].unique().tolist(),
        default=df["card_type"].unique().tolist()
    )

    # User ID dropdown
    user_filter = st.sidebar.selectbox(
        "User ID",
        options=["All"] + sorted(df["user_id"].unique().tolist())
    )

    # Apply filters
    filtered_df = df[
        (df["amount"] >= min_amt) &
        (df["amount"] <= max_amt) &
        (df["card_type"].isin(card_types))
    ]

    if user_filter != "All":
        filtered_df = filtered_df[filtered_df["user_id"] == user_filter]


    # --- METRICS ---

    csv = filtered_df.to_csv(index=False)
    download_button = st.download_button(
        label="📤 Download Filtered Transactions as CSV",
        data=csv,
        file_name="flagged_transactions.csv",
        mime="text/csv",
    )

    st.divider()
    col1, col2 = st.columns(2)
    col1.metric("🔁 Total Transactions", all_txns.count_documents({}))
    col2.metric("🚨 Flagged as Fraud", flagged_txns.count_documents({}))

    # --- CHARTS ---
    st.divider()

    # Line chart: fraud amount over time
    time_series = (
        filtered_df.groupby(pd.Grouper(key="timestamp", freq="1min"))["amount"]
        .sum()
        .reset_index()
    )
    st.markdown("#### 📈 Total Fraud Amount Over Time (1-min buckets)")
    st.line_chart(time_series.rename(columns={"timestamp": "index"}).set_index("index"))

    # Bar chart: top flagged users
    st.markdown("#### 📊 Top 10 Fraudster User IDs (by frequency)")
    top_users = filtered_df["user_id"].value_counts().head(10)
    st.bar_chart(top_users)

    # --- TABLE ---
    st.divider()
    st.markdown("#### 📋 Most Recent Flagged Transactions (last 50)")

    df_sorted = filtered_df.sort_values(by="timestamp", ascending=False)
    columns_to_show = ["timestamp", "user_id", "amount", "card_type", "location"]
    for col in columns_to_show:
        if col not in df_sorted.columns:
            df_sorted[col] = "N/A"

    st.dataframe(df_sorted[columns_to_show].head(50), use_container_width=True)
