# Real-Time Fraud Detection
This project simulates a payment system (like ACH/Wire/Credit Card) where transactions stream in real-time.

✅ PHASE 1: 🧱 Setup & Simulation
 Setup project structure and README

 Generate dummy real-time transactions (Python script + Faker)

 Send transactions into Kafka

✅ PHASE 2: 🔥 Real-Time Processing
 Process data using Spark Streaming or Flink

 Apply simple fraud rules (e.g., too many transactions, large amount, IP/Geo mismatch)

✅ PHASE 3: 📦 Storage & Output
 Write flagged data to MongoDB (or Postgres)

 Write all data (cleaned + flagged) to AWS S3 in Parquet

 Optionally use Delta Lake for versioned storage

✅ PHASE 4: 📊 Analytics & Visualization
 Use Databricks notebooks to analyze and visualize

 Show number of frauds, common IPs, user patterns

✅ PHASE 5: ☁️ Scaling & Cloud
 Run Spark job on AWS EMR or Databricks

 Use Docker to containerize services

 Add optional AWS Glue job to clean batch data


   +------------------------+     
  |  Fake Transaction Gen  |     ← Python script using Faker
  +-----------+------------+     
              |
              v
       +------+--------+          
       |    Kafka      |     ← Real-time message broker
       +------+--------+          
              |
              v
   +----------+-----------+       
   | Spark Streaming Job  |     ← Detect fraud in real-time
   +----------+-----------+       
     |                    |
     v                    v
+---------+         +------------+
| MongoDB |         |  AWS S3    |   ← Store flagged & all transactions
+---------+         +------------+
                         |
                         v
                  +--------------+
                  | Databricks   |   ← Visualize patterns
                  +--------------+
