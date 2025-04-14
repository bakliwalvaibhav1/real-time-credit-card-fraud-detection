# 🚨 Real-Time Fraud Detection Pipeline 🛡️

A production-grade, cloud-deployable pipeline that simulates and detects financial fraud in real time using Kafka, Python, and MongoDB. The pipeline processes transactions and flags suspicious activity such as high-frequency or high-value anomalies. Streamlit is used to visualize flagged transactions via a live dashboard.

## ✨ Features

- ⏰ Real-time data streaming using Kafka (KRaft mode)
- 💸 Transaction generator producing realistic financial events
- 🚨 Fraud detection engine using Python consumers with customizable rules
- 📀 MongoDB for persistent storage of flagged transactions
- 📊 Live dashboard powered by Streamlit
- ⬇️ Download Filtered transactions as CSV
- ⛴️ Docker Compose setup for modular microservice deployment
- 📦 Deployment ready infrastructure

## 🧱 Architecture

- **Producer**: Generates synthetic transaction data and streams to Kafka
- **Consumer**: Listens to Kafka, applies fraud rules, and stores flagged data in MongoDB
- **MongoDB**: Stores only fraudulent transactions for lightweight querying
- **Streamlit Dashboard**: Auto-refreshing UI displaying flagged transactions in real time

## 🛠️ Technologies Used
![My Skills](https://skillicons.dev/icons?i=kafka,python,mongo,docker,aws&theme=light)
- Kafka 4.0
- Python 3.10+
- MongoDB
- Streamlit
- Docker + Docker Compose
- AWS EC2 (Or any other VM)

## 📁 Project Structure

```bash
.
├── consumer/
│   ├── consume_from_kafka.py
│   ├── fraud_rules.py
│   ├── requirements.txt
│   └── Dockerfile
├── dashboard/
│   ├── streamlit_app.py
│   ├── requirements.txt
│   └── Dockerfile
├── producer/
│   ├── send_to_kafka.py
│   ├── generate_transactions.py
│   ├── historical_generate.py
│   ├── test_mongo.py
│   ├── requirements.txt
│   └── Dockerfile
├── storage/(for parquet files)
│   ├── filtered/
│   ├── exported/
│   ├── historical/
│   └── export_to_parquet.py
├── docker-compose.prod.yml
├── .gitignore
└── README.md
```

## 🚀 Quick Start (Local or VM)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/real-time-fraud-detection.git
```

```bash
cd real-time-fraud-detection
```

### 2. Build and run with Docker Compose

```bash
sudo docker-compose -f docker-compose.prod.yml up --build
```

### 3. Access the dashboard

```bash
http://localhost:8501
# Or on VM:
http://<your-VM-public-ip>:8501
```

## 🧠 Fraud Detection Rules

- **Rule 1 - High Amount Rule**: Flags any transaction above a set threshold (e.g., $1000)
- **Rule 2 - High Frequency Rule**: Flags if a user transacts too frequently in a short span
- **Rule 3 - Unusual Hour**: Flags if the transaction occurs during unsual hours
- **Rule 4 - Geo Mismatch Rule**: Flags if the location of the user is changed quickly between 2 transactions.

## 📦 Historical Data

- Use the script - producer/historical_generate.py,to generate historical data.
- Over 47 million transactions generated from 2000–2025.
- Stored in partitioned Parquet format in `storage/historical/`.
- Suitable for batch analytics, ML, or S3 → Athena usage.

## ☁️ Cloud Deployment

- Use any Virtual Machine eg-AWS EC2, Azure VM, Google Compute Engine, etc
- SSH into instance
- Clone the repo
- Install Docker and Docker Compose
- Use `docker-compose.prod.yml` to deploy everything in one command

## 📈 Dashboard Preview

Displays:
- 📊 Amount over time
- 🔝 Top flagged users
- 🧾 Latest flagged transactions

Auto-refreshes every second using `streamlit-autorefresh`.
