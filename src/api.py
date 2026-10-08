from fastapi import FastAPI, HTTPException
import pandas as pd


DATA_FILE = "data/gold/final_anomaly_results.csv"


app = FastAPI(
    title="Real-Time Transaction Monitoring API",
    description="API for transaction anomaly detection and risk monitoring",
    version="1.0.0"
)


def load_data():
    return pd.read_csv(DATA_FILE)


@app.get("/")
def root():
    return {
        "message": "Transaction Monitoring API is running"
    }


@app.get("/transactions")
def get_transactions():

    df = load_data()

    return {
        "total_transactions": len(df),
        "transactions": df.to_dict(orient="records")
    }


@app.get("/anomalies")
def get_anomalies():

    df = load_data()

    anomalies = df[df["anomaly_prediction"] == -1]

    return {
        "total_anomalies": len(anomalies),
        "anomalies": anomalies.to_dict(orient="records")
    }


@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: int):

    df = load_data()

    transaction = df[
        df["transaction_id"] == transaction_id
    ]

    if transaction.empty:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction.iloc[0].to_dict()


@app.get("/stats")
def get_stats():

    df = load_data()

    return {
        "total_transactions": len(df),
        "total_anomalies": int(
            (df["anomaly_prediction"] == -1).sum()
        ),
        "critical_transactions": int(
            (df["risk_level"] == "CRITICAL").sum()
        ),
        "high_risk_transactions": int(
            (df["risk_level"] == "HIGH").sum()
        ),
        "medium_risk_transactions": int(
            (df["risk_level"] == "MEDIUM").sum()
        ),
        "low_risk_transactions": int(
            (df["risk_level"] == "LOW").sum()
        )
    }
