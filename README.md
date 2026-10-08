# 🏦 Real-Time Transaction Monitoring System

> **End-to-end banking transaction monitoring pipeline using Kafka, Spark, Machine Learning, FastAPI, Streamlit, and Docker.**

A portfolio-grade data engineering + machine learning project that simulates a banking transaction monitoring system. Transactions flow through an ingestion and processing pipeline, are cleaned and enriched through Bronze/Silver/Gold layers, analyzed with Apache Spark, scored for anomalies using an Isolation Forest model, and exposed through a REST API and interactive monitoring dashboard.

---

## 🚀 What This Project Does

The system takes transaction data from generation to risk visualization:

```text
                    TRANSACTION MONITORING PIPELINE

  ┌──────────────────┐
  │ Transaction      │
  │ Generator        │
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │ Apache Kafka      │
  │ Event Streaming   │
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │ Bronze Layer      │
  │ Raw Ingestion     │
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │ Silver Layer      │
  │ Clean + Validate  │
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │ Gold Layer        │
  │ Analytics + ML    │
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │ Apache Spark      │
  │ Feature Processing│
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │ Isolation Forest  │
  │ Anomaly Detection │
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │ Risk Scoring      │
  │ LOW → CRITICAL    │
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │ FastAPI           │
  │ REST API          │
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │ Streamlit         │
  │ Monitoring UI     │
  └──────────────────┘
```

---

## ✨ Highlights

- 📡 **Event streaming** with Apache Kafka
- 🧹 **Data quality pipeline** with validation and cleaning
- 🥉 **Bronze / Silver / Gold** data architecture
- ⚡ **Apache Spark** for scalable feature processing
- 🤖 **Unsupervised anomaly detection** using Isolation Forest
- 📊 **Relative risk scoring** from anomaly scores
- 🚨 Risk classification: **LOW / MEDIUM / HIGH / CRITICAL**
- 🔌 **FastAPI REST API** with Swagger documentation
- 📈 **Streamlit dashboard** for transaction monitoring
- 🐳 **Dockerized services**
- 🔧 Built and tested locally with Python, Docker Desktop, and Windows/WSL2

---

# 🏗️ System Architecture

```text
                           ┌─────────────────────┐
                           │ Transaction Generator│
                           └──────────┬──────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │       KAFKA         │
                           │   transactions      │
                           └──────────┬──────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │      BRONZE         │
                           │   Raw JSONL Data    │
                           └──────────┬──────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │      SILVER         │
                           │ Clean + Validate    │
                           └──────────┬──────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │       GOLD          │
                           │ Analytics Features  │
                           └──────────┬──────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │       SPARK         │
                           │ Batch Processing    │
                           └──────────┬──────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │   ML FEATURE SET    │
                           └──────────┬──────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │  ISOLATION FOREST   │
                           │ Anomaly Detection   │
                           └──────────┬──────────┘
                                      │
                                      ▼
                           ┌─────────────────────┐
                           │    RISK SCORING     │
                           └──────────┬──────────┘
                                      │
                                      ▼
                    ┌────────────────────────────────┐
                    │            FASTAPI             │
                    │      REST API + Swagger        │
                    └───────────────┬────────────────┘
                                    │
                                    ▼
                    ┌────────────────────────────────┐
                    │          STREAMLIT              │
                    │      Monitoring Dashboard      │
                    └────────────────────────────────┘
```

---

# 🧰 Tech Stack

| Category | Technology |
|---|---|
| Programming | Python |
| Streaming | Apache Kafka |
| Data Processing | Pandas, NumPy |
| Distributed Processing | Apache Spark / PySpark |
| Machine Learning | Scikit-learn |
| Anomaly Detection | Isolation Forest |
| Backend | FastAPI |
| API Server | Uvicorn |
| Dashboard | Streamlit |
| Containerization | Docker, Docker Compose |
| Version Control | Git, GitHub |
| API Documentation | Swagger / OpenAPI |

---

# 📂 Project Structure

```text
real-time-transaction-monitoring/
│
├── data/
│   ├── raw/                    # Generated raw transactions
│   ├── processed/              # Initial processed data
│   ├── bronze/                 # Kafka-ingested raw data
│   ├── silver/                 # Cleaned and validated data
│   └── gold/                   # Analytics + ML-ready data
│
├── src/
│   ├── generate_data.py        # Transaction generator
│   ├── etl.py                  # Initial ETL pipeline
│   │
│   ├── kafka_producer.py       # Publishes transactions to Kafka
│   ├── kafka_consumer.py       # Kafka consumer
│   ├── kafka_bronze_consumer.py# Stores Kafka events in Bronze
│   │
│   ├── silver_processing.py    # Data cleaning + validation
│   ├── gold_processing.py      # Analytics feature engineering
│   ├── spark_processing.py     # Spark transformations
│   │
│   ├── anomaly_detection.py    # Creates ML feature dataset
│   ├── train_anomaly_model.py  # Isolation Forest training
│   ├── risk_scoring.py         # Converts anomaly scores to risk
│   │
│   ├── api.py                  # FastAPI application
│   └── dashboard.py            # Streamlit dashboard
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🔄 Data Engineering Pipeline

## 1. Transaction Generation

Synthetic banking transactions are generated with fields such as:

```text
transaction_id
customer_id
amount
location
timestamp
merchant
```

The generator also introduces intentionally problematic records to validate the pipeline.

Examples include:

- Duplicate transactions
- Missing customer IDs
- Missing amounts
- Negative amounts
- Invalid timestamps
- High-value transactions

This makes the pipeline more representative of real-world data quality problems.

---

## 2. Kafka — Event Ingestion

Transactions are published to the Kafka topic:

```text
transactions
```

Kafka acts as the event-streaming layer between transaction generation and downstream storage/processing.

```text
Producer
   │
   ▼
Kafka Topic: transactions
   │
   ├── Consumer
   │
   └── Bronze Consumer
```

The topic is configured with multiple partitions to demonstrate Kafka's distributed event-streaming model.

---

# 🥉 3. Bronze Layer

The Bronze layer stores the data received from Kafka with minimal transformation.

```text
data/bronze/transactions.jsonl
```

The goal is to preserve what arrived from the ingestion layer before applying data-quality transformations.

**Bronze = raw-ish ingestion**

---

# 🥈 4. Silver Layer

The Silver layer creates a trusted dataset.

The pipeline performs:

- Duplicate removal
- Amount type conversion
- Positive amount validation
- Missing customer validation
- Timestamp validation
- Date extraction
- Hour extraction
- High-value transaction flag creation

Example validation logic:

```text
amount > 0
customer_id != null
timestamp is valid
transaction_id is unique
```

**Silver = clean + validated data**

---

# 🥇 5. Gold Layer

The Gold layer contains analytics and machine-learning-ready features.

Customer-level features include:

```text
customer_avg_amount
customer_max_amount
customer_transaction_count
amount_vs_customer_avg
amount_log
is_high_value
```

**Gold = analytics + ML-ready data**

---

# ⚡ Apache Spark

Apache Spark processes the curated transaction data and calculates customer-level aggregations.

The Spark pipeline:

1. Reads Silver transaction data
2. Groups transactions by customer
3. Calculates customer statistics
4. Joins statistics back to transactions
5. Creates derived features
6. Writes the Gold/Spark output

For local development:

```python
.master("local[*]")
```

This uses Spark's local execution mode while preserving the same Spark programming model used in larger distributed environments.

---

# 🤖 Machine Learning

## Why Anomaly Detection?

Traditional fraud classification requires labelled historical fraud data.

This project demonstrates an **unsupervised** approach because the synthetic transaction dataset does not provide a large labelled fraud dataset.

## Isolation Forest

The project uses:

```python
IsolationForest(
    n_estimators=200,
    contamination=0.02,
    random_state=42
)
```

### Features

The model uses:

```text
amount
amount_log
customer_avg_amount
customer_max_amount
customer_transaction_count
amount_vs_customer_avg
```

Transaction and customer IDs are retained for traceability but are **not used as model features**.

### Output

Isolation Forest produces:

```text
 1  → Normal
-1  → Anomaly
```

---

# 🚨 Risk Scoring

The anomaly score is converted into a normalized relative risk score:

```text
0 ─────────────────────────────── 100
LOW                              CRITICAL
```

Risk categories:

| Risk Score | Risk Level |
|---:|---|
| 0–39 | 🟢 LOW |
| 40–69 | 🟡 MEDIUM |
| 70–89 | 🟠 HIGH |
| 90–100 | 🔴 CRITICAL |

> **Note:** The risk score is a normalized monitoring score, not a calibrated probability of fraud.

---

# 📊 Current Results

The synthetic dataset used during development contains:

```text
Raw transactions             1007
Unique transaction IDs       1006
Clean Silver transactions    1002
Detected anomalies           21
```

The dataset includes two intentionally suspicious high-value transactions:

```text
Transaction 1001 → ₹500,000
Transaction 1002 → ₹750,000
```

Both were detected by the anomaly detection pipeline.

The configured Isolation Forest contamination is approximately **2%**, resulting in 21 detected anomalies for the 1002-record clean dataset.

---

# 🔌 FastAPI

The FastAPI application exposes the processed results through REST endpoints.

Start locally:

```powershell
python -m uvicorn src.api:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | API health check |
| `GET` | `/transactions` | Retrieve all transactions |
| `GET` | `/anomalies` | Retrieve detected anomalies |
| `GET` | `/transactions/{transaction_id}` | Retrieve a specific transaction |
| `GET` | `/stats` | Retrieve monitoring statistics |

Example:

```text
GET /transactions/1001
```

---

# 📈 Streamlit Dashboard

The dashboard provides a monitoring interface on top of the FastAPI service.

It displays:

### Overview

- Total transactions
- Total anomalies
- Critical transactions
- High-risk transactions

### Risk Distribution

```text
CRITICAL
HIGH
MEDIUM
LOW
```

### Anomaly Table

The dashboard exposes:

```text
transaction_id
customer_id
amount
anomaly_score
risk_score
risk_level
```

### Transaction Lookup

A user can enter a transaction ID and retrieve its complete information through the FastAPI backend.

Start locally:

```powershell
python -m streamlit run src/dashboard.py
```

Dashboard:

```text
http://localhost:8501
```

---

# 🐳 Docker

The project uses Docker Compose to run the application services.

Current containerized architecture:

```text
┌───────────────────────────────────────────┐
│              Docker Desktop               │
│                                           │
│  ┌─────────────┐                          │
│  │    Kafka    │ :9092                    │
│  └─────────────┘                          │
│                                           │
│  ┌─────────────┐                          │
│  │   FastAPI   │ :8000                    │
│  └─────────────┘                          │
│                                           │
│  ┌─────────────┐                          │
│  │  Streamlit  │ :8501                    │
│  └─────────────┘                          │
│                                           │
└───────────────────────────────────────────┘
```

## Start Kafka

```powershell
docker compose up -d kafka
```

## Build API

```powershell
docker compose build api
```

## Start API

```powershell
docker compose up -d api
```

## Build Dashboard

```powershell
docker compose build dashboard
```

## Start Dashboard

```powershell
docker compose up -d dashboard
```

## Check Containers

```powershell
docker compose ps
```

Expected services:

```text
transaction-kafka
transaction-api
transaction-dashboard
```

---

# 🧪 Running the Project Locally

## Prerequisites

Install:

- Python 3.11
- Docker Desktop
- Git
- Java 17+ for Spark
- Apache Kafka through Docker

## 1. Clone

```bash
git clone https://github.com/ojaswip2828/real-time-transaction-monitoring.git
cd real-time-transaction-monitoring
```

## 2. Create Virtual Environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

## 4. Start Kafka

```powershell
docker compose up -d kafka
```

## 5. Run the Data Pipeline

Run the project components in their intended pipeline order:

```text
Generate Transactions
        ↓
Kafka Producer
        ↓
Kafka Bronze Consumer
        ↓
Silver Processing
        ↓
Gold Processing
        ↓
Spark Processing
        ↓
ML Feature Generation
        ↓
Anomaly Detection
        ↓
Risk Scoring
```

## 6. Start API

```powershell
python -m uvicorn src.api:app --reload
```

## 7. Start Dashboard

Open another terminal:

```powershell
.\venv\Scripts\Activate.ps1
python -m streamlit run src/dashboard.py
```

---

# 🔍 Example End-to-End Flow

A transaction moves through the system like this:

```text
₹750,000 transaction
        ↓
Kafka
        ↓
Bronze
        ↓
Silver validation
        ↓
Gold feature engineering
        ↓
Spark processing
        ↓
Isolation Forest
        ↓
Anomaly detected
        ↓
Risk score calculated
        ↓
FastAPI
        ↓
Streamlit
        ↓
🚨 Transaction displayed as anomalous
```

---

# 🧠 Engineering Concepts Demonstrated

This project demonstrates practical implementation of:

### Data Engineering

- ETL
- Data validation
- Event streaming
- Kafka consumers/producers
- Medallion architecture
- Batch processing
- Feature engineering

### Big Data

- Apache Spark
- Distributed-processing concepts
- Customer-level aggregations

### Machine Learning

- Unsupervised learning
- Isolation Forest
- Feature engineering
- Anomaly scoring
- Risk classification

### Backend

- REST APIs
- FastAPI
- Swagger/OpenAPI
- API-to-dashboard communication

### DevOps

- Docker
- Docker Compose
- Container networking
- Git/GitHub

---

# 📌 Design Decisions

### Why Kafka?

To introduce an event-streaming layer and decouple transaction generation from downstream processing.

### Why Bronze/Silver/Gold?

To separate raw ingestion, trusted cleaned data, and analytics/ML-ready data.

### Why Spark?

To demonstrate how the transformation layer can scale from local processing toward distributed data processing.

### Why Isolation Forest?

Because the demonstration dataset does not depend on labelled fraud examples, making an unsupervised anomaly detector appropriate for the prototype.

### Why FastAPI?

To expose model outputs and transaction information through a lightweight REST interface.

### Why Streamlit?

To quickly build an interactive monitoring interface on top of the API.

### Why Docker?

To make the application services reproducible and simplify local deployment.

---

# 📈 Future Improvements

The prototype can be extended toward a production architecture by adding:

- Real banking transaction streams
- Distributed Kafka deployment
- Spark cluster deployment
- Persistent data lake/lakehouse storage
- Data warehouse
- Historical fraud-labelled training data
- Model retraining pipeline
- Model drift monitoring
- Feature store
- Authentication and role-based access
- Automated unit/integration tests
- CI/CD pipeline
- Real-time alerting
- Email/SMS/Slack alerts for critical transactions
- Cloud deployment
- Infrastructure as Code

---

# ⚠️ Disclaimer

This is an **educational and portfolio project** using synthetic banking transaction data.

The anomaly and risk scores demonstrate the mechanics of a transaction monitoring system and should **not** be interpreted as production fraud decisions or calibrated fraud probabilities.

---

# 👩‍💻 Author

**Ojaswi**

Electronics & Communication Engineering  
Nitte Meenakshi Institute of Technology, Bengaluru

GitHub:  
https://github.com/ojaswip2828

---

## ⭐ If you found this project useful

Feel free to explore the code, experiment with the transaction generator, modify the anomaly detection features, and extend the pipeline toward a fully deployed real-time fraud monitoring platform.
