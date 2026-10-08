Real-Time Transaction Monitoring System
An end-to-end banking transaction monitoring system that ingests transaction data, processes it through a Bronze/Silver/Gold data pipeline, performs Spark-based analytics, detects anomalous transactions using an Isolation Forest model, assigns risk scores, and exposes the results through a FastAPI backend and Streamlit dashboard.
Architecture
Transaction Generator
        |
        v
      Kafka
        |
        v
     Bronze
        |
        v
     Silver
        |
        v
      Gold
        |
        v
      Spark
        |
        v
ML Feature Dataset
        |
        v
Isolation Forest
        |
        v
   Risk Scoring
        |
        v
     FastAPI
        |
        v
   Streamlit Dashboard
Key Features
- Synthetic banking transaction generation
- Kafka-based transaction ingestion
- Bronze, Silver, and Gold data layers
- Data cleaning and validation with Pandas
- Spark-based batch processing
- Customer-level transaction feature engineering
- Unsupervised anomaly detection using Isolation Forest
- Risk score generation from anomaly scores
- Risk classification: LOW, MEDIUM, HIGH, CRITICAL
- REST API using FastAPI
- Interactive monitoring dashboard using Streamlit
- Dockerized Kafka, FastAPI, and Streamlit services
- Swagger/OpenAPI documentation
Technology Stack
Area	Technology
Language	Python
Data Processing	Pandas, NumPy
Streaming	Apache Kafka
Distributed Processing	Apache Spark / PySpark
Machine Learning	Scikit-learn
Anomaly Detection	Isolation Forest
Backend	FastAPI
Dashboard	Streamlit
Containerization	Docker, Docker Compose
Version Control	Git, GitHub


Data Pipeline
1. Transaction Generation
The transaction generator creates synthetic banking transactions containing fields such as:
- transaction_id
- customer_id
- amount
- location
- timestamp
- merchant
The dataset also includes intentionally dirty records to test the data-quality pipeline.
2. Kafka Ingestion
Transactions are published to a Kafka topic named:
transactions
Kafka is used as the event-streaming layer between transaction generation and downstream processing.
3. Bronze Layer
The Bronze layer stores the transaction data received from Kafka in JSONL format.
Example:
data/bronze/transactions.jsonl
This layer represents the raw ingestion stage.
4. Silver Layer
The Silver processing pipeline cleans and validates the Bronze data.
Operations include:
- Removing duplicate transaction IDs
- Converting transaction amounts to numeric values
- Removing missing customer IDs
- Removing invalid timestamps
- Removing non-positive transaction amounts
- Creating date/hour features
- Creating high-value transaction indicators
The resulting clean dataset is stored under:
data/silver/
5. Gold Layer
The Gold layer contains analytics-ready and ML-ready transaction data.
Customer-level features include:
- Customer average transaction amount
- Customer maximum transaction amount
- Customer transaction count
- Amount compared with customer average
- Log-transformed transaction amount
- High-value transaction indicator
The ML feature dataset is generated from the Gold data.
Spark Processing
Apache Spark is used to demonstrate scalable batch processing.
The Spark job:
1. Reads Silver transaction data
2. Calculates customer-level aggregations
3. Joins the statistics back to transactions
4. Creates analytical features
5. Writes the resulting Gold dataset
The project uses:
.master("local[*]")
for local development, allowing Spark to use the available CPU cores on the development machine.
Machine Learning
Isolation Forest
The project uses Scikit-learn's IsolationForest for unsupervised anomaly detection.
This approach is useful for transaction monitoring because the synthetic dataset does not contain a large labelled fraud dataset.
Model configuration:
IsolationForest(
    n_estimators=200,
    contamination=0.02,
    random_state=42
)
The model uses features including:
- Transaction amount
- Log transaction amount
- Customer average amount
- Customer maximum amount
- Customer transaction count
- Amount versus customer average
Transaction and customer IDs are retained for traceability but are not used as model features.
Anomaly Output
The model produces:
1  -> Normal
-1 -> Anomaly
The anomaly score is then converted into a relative risk score between 0 and 100.
Risk Levels
90 - 100  → CRITICAL
70 - 89   → HIGH
40 - 69   → MEDIUM
0  - 39   → LOW
The risk score is a normalized monitoring score rather than a calibrated probability of fraud.
FastAPI
The processed anomaly results are exposed through a REST API.
Run locally with:
python -m uvicorn src.api:app --reload
API documentation:
http://127.0.0.1:8000/docs
API Endpoints
Method	Endpoint	Purpose
GET	/	API health check
GET	/transactions	Retrieve all transactions
GET	/anomalies	Retrieve detected anomalies
GET	/transactions/{transaction_id}	Retrieve one transaction
GET	/stats	Retrieve monitoring statistics


Example:
GET /transactions/1001
Streamlit Dashboard
The Streamlit dashboard provides a visual monitoring interface.
It displays:
- Total transactions
- Number of anomalies
- Critical transactions
- High-risk transactions
- Risk distribution
- Detected anomalous transactions
- Transaction lookup
Run locally with:
python -m streamlit run src/dashboard.py
Dashboard:
http://localhost:8501
Docker
The project includes Docker Compose configuration for:
- Apache Kafka
- FastAPI
- Streamlit
Start Kafka:
docker compose up -d kafka
Build the API:
docker compose build api
Start the API:
docker compose up -d api
Build and start the dashboard:
docker compose build dashboard
docker compose up -d dashboard
Check running services:
docker compose ps
Expected services:
transaction-kafka
transaction-api
transaction-dashboard
Dockerized endpoints:
FastAPI:
http://localhost:8000/docs

Streamlit:
http://localhost:8501
Project Structure
real-time-transaction-monitoring/
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── bronze/
│   ├── silver/
│   └── gold/
│
├── src/
│   ├── generate_data.py
│   ├── etl.py
│   ├── kafka_producer.py
│   ├── kafka_consumer.py
│   ├── kafka_bronze_consumer.py
│   ├── silver_processing.py
│   ├── gold_processing.py
│   ├── spark_processing.py
│   ├── anomaly_detection.py
│   ├── train_anomaly_model.py
│   ├── risk_scoring.py
│   ├── api.py
│   └── dashboard.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .gitignore
Local Setup
1. Clone the repository
git clone https://github.com/ojaswip2828/real-time-transaction-monitoring.git
cd real-time-transaction-monitoring
2. Create a virtual environment
Windows PowerShell:
python -m venv venv
.\venv\Scripts\Activate.ps1
3. Install dependencies
pip install -r requirements.txt
4. Start Kafka
Make sure Docker Desktop is running:
docker compose up -d kafka
5. Run the processing pipeline
The project scripts can be executed in the appropriate pipeline order:
Transaction Generation
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
Anomaly Model
        ↓
Risk Scoring
6. Start FastAPI
python -m uvicorn src.api:app --reload
7. Start Streamlit
Open another terminal:
.\venv\Scripts\Activate.ps1
python -m streamlit run src/dashboard.py
Example Monitoring Flow
A suspicious transaction can move through the system as:
Transaction
    ↓
Kafka
    ↓
Bronze ingestion
    ↓
Data validation
    ↓
Silver dataset
    ↓
Gold feature engineering
    ↓
Isolation Forest
    ↓
Anomaly detected
    ↓
Risk score
    ↓
FastAPI
    ↓
Streamlit dashboard
Project Results
The current synthetic dataset contains:
- 1007 raw transaction records
- 1006 unique transaction IDs before cleaning
- 1002 clean Silver records after validation
- 21 model-detected anomalies using the configured 2% contamination level
Two intentionally suspicious high-value transactions were included in the dataset and were detected by the anomaly detection pipeline.
Engineering Concepts Demonstrated
This project demonstrates practical experience with:
- Event-driven data ingestion
- Data quality and validation
- ETL pipelines
- Medallion-style data architecture
- Batch processing with Spark
- Feature engineering
- Unsupervised machine learning
- Anomaly detection
- REST API development
- Dashboard development
- Containerization
- Docker networking
- Git/GitHub workflows
Future Improvements
Potential production-oriented improvements include:
- Replace synthetic data with a real transaction stream
- Run Spark in a distributed cluster
- Add a persistent data warehouse/lakehouse
- Use a feature store for ML features
- Train on historical fraud-labelled data when available
- Add model monitoring and drift detection
- Add authentication and role-based access to the API
- Add automated tests and CI/CD
- Deploy Kafka and processing services to cloud infrastructure
- Add real-time alerting for critical transactions
- Deploy the dashboard and API publicly
Disclaimer
This project is an educational/portfolio implementation using synthetic transaction data. The anomaly score and risk score are intended for demonstration and are not a production fraud-detection decision system.