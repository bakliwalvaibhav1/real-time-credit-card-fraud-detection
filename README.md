# 🛡️ Real-Time Fraud Detection Pipeline

A full-featured real-time data engineering project that detects suspicious financial transactions as they stream in, using Kafka, Python, and MongoDB.

---

## 📐 Architecture Overview

```bash
+------------------------+     
|  Fake Transaction Gen  |     ← Python + Faker
+-----------+------------+     
            |
            v
     +------+--------+          
     |    Kafka      |     ← Streams transactions
     +------+--------+          
            |
            v
+-----------+------------+
| Python Consumer (Kafka)|
|  - Applies rules       |
|  - Stores in MongoDB   |
+------+--------+--------+
       |                 |
       v                 v
+------------+     +-----------------------+
| transactions |     | flagged_transactions |
| (all txns)   |     | (suspicious only)    |
+--------------+     +----------------------+
```

---

## 💻 Tech Stack

| Tool         | Purpose                           |
|--------------|-----------------------------------|
| ```Kafka```      | Real-time message broker          |
| ```Python```     | Kafka producer & consumer logic   |
| ```Faker```      | Fake transaction generator        |
| ```MongoDB```    | Data storage for analysis         |
| ```Docker```     | Containerized services            |
| ```kafka-python``` | Kafka interaction client         |
| ```pymongo```    | MongoDB client library            |

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/real-time-fraud-detection.git
cd real-time-fraud-detection
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate   # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Kafka and MongoDB

```bash
cd kafka/
docker compose up -d
```

---

## ⚙️ How to Run It

### Start the Transaction Producer
```bash
python producer/send_to_kafka.py
```

### Start the Fraud Detection Consumer
```bash
python producer/consume_from_kafka.py
```

### View Data in MongoDB

To open a Mongo shell:

```bash
docker exec -it mongodb mongosh frauddb
```

Then in shell:

```bash
db.transactions.find().pretty()
db.flagged_transactions.find().pretty()
```

---

## 🔍 Current Fraud Detection Rules

| Rule              | Description                                             |
|-------------------|---------------------------------------------------------|
| **High Amount**   | Flags if ```amount > 900```                                 |
| **High Frequency**| Flags if user makes ≥ 3 transactions within 10 seconds |

---

## 🗺️ Roadmap / TODO

- [ ] Add ```Unusual Hour``` detection (e.g. transactions between midnight–5am)
- [ ] Add ```Geo Mismatch``` rule (same user in different countries)
- [ ] Add ```Merchant Risk Category``` rule
- [ ] Simulate ```device_id```, ```ip_address```, ```location``` in data
- [ ] Store suspicious device/IPs
- [ ] Add Delta Lake or S3 export
- [ ] Visualize data in Streamlit or Dash

---

## 🧪 Testing Ideas

- Reduce ```sleep()``` in producer to simulate rapid-fire attacks
- Insert fake bad transactions with weird values (e.g., negative amount)
- Observe flagged output live while messages stream in
