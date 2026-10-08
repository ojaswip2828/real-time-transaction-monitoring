import pandas as pd
import os

GOLD_FILE = "data/gold/transaction_features.csv"
ML_FILE = "data/gold/ml_features.csv"


def load_data():
    print("Loading Gold data...")

    df = pd.read_csv(GOLD_FILE)

    print(f"Loaded {len(df)} transactions.")

    return df


def prepare_features(df):
    print("Preparing ML features...")

    features = df[
        [
            "transaction_id",
            "customer_id",
            "amount",
            "amount_log",
            "customer_avg_amount",
            "customer_max_amount",
            "customer_transaction_count",
            "amount_vs_customer_avg"
        ]
    ].copy()

    print("Selected ML features:")
    print(features.columns.tolist())

    return features


def save_features(features):
    print("Saving ML dataset...")

    os.makedirs("data/gold", exist_ok=True)

    features.to_csv(ML_FILE, index=False)

    print(f"Saved ML dataset to: {ML_FILE}")
    print(f"ML records: {len(features)}")


def main():

    df = load_data()

    features = prepare_features(df)

    save_features(features)

    print("ML feature preparation completed.")


if __name__ == "__main__":
    main()