import pandas as pd
import os

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


ML_FILE = "data/gold/ml_features.csv"
OUTPUT_FILE = "data/gold/anomaly_results.csv"


def load_data():
    print("Loading ML dataset...")

    df = pd.read_csv(ML_FILE)

    print(f"Loaded {len(df)} transactions.")

    return df


def train_model(df):

    print("Preparing features...")

    feature_columns = [
        "amount",
        "amount_log",
        "customer_avg_amount",
        "customer_max_amount",
        "customer_transaction_count",
        "amount_vs_customer_avg"
    ]

    X = df[feature_columns]

    print("Scaling features...")

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    print("Training Isolation Forest...")

    model = IsolationForest(
        n_estimators=200,
        contamination=0.02,
        random_state=42
    )

    model.fit(X_scaled)

    predictions = model.predict(X_scaled)
    scores = model.decision_function(X_scaled)

    df["anomaly_prediction"] = predictions
    df["anomaly_score"] = scores

    return df


def save_results(df):

    print("Saving anomaly results...")

    os.makedirs("data/gold", exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved results to: {OUTPUT_FILE}")


def show_anomalies(df):

    anomalies = df[df["anomaly_prediction"] == -1]

    print("\n===== ANOMALIES DETECTED =====")

    print(f"Total anomalies: {len(anomalies)}")

    print(
        anomalies[
            [
                "amount",
                "amount_vs_customer_avg",
                "anomaly_score",
                "anomaly_prediction"
            ]
        ]
        .sort_values("anomaly_score")
        .head(20)
    )


def main():

    df = load_data()

    df = train_model(df)

    show_anomalies(df)

    save_results(df)

    print("\nAnomaly detection completed.")


if __name__ == "__main__":
    main()