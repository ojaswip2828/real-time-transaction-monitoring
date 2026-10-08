import pandas as pd
import os


SILVER_FILE = "data/silver/clean_transactions.csv"
GOLD_FILE = "data/gold/transaction_features.csv"


def extract_silver():

    print("Reading Silver data...")

    df = pd.read_csv(
        SILVER_FILE,
        parse_dates=["timestamp"]
    )

    print(f"Read {len(df)} Silver records.")

    return df


def create_features(df):

    print("Creating Gold features...")

    # Transaction amount features
    df["amount_log"] = (
        df["amount"].apply(lambda x: __import__("math").log1p(x))
    )

    # Customer transaction statistics
    customer_avg = (
        df.groupby("customer_id")["amount"]
        .transform("mean")
    )

    customer_max = (
        df.groupby("customer_id")["amount"]
        .transform("max")
    )

    customer_count = (
        df.groupby("customer_id")["transaction_id"]
        .transform("count")
    )

    df["customer_avg_amount"] = customer_avg

    df["customer_max_amount"] = customer_max

    df["customer_transaction_count"] = customer_count

    # Compare transaction with customer's average
    df["amount_vs_customer_avg"] = (
        df["amount"] / df["customer_avg_amount"]
    )

    # High-value transaction
    df["is_high_value"] = (
        df["amount"] > 10000
    )

    return df


def validate(df):

    print("Validating Gold data...")

    required_features = [
        "amount",
        "amount_log",
        "customer_avg_amount",
        "customer_max_amount",
        "customer_transaction_count",
        "amount_vs_customer_avg",
        "is_high_value"
    ]

    for column in required_features:

        if column not in df.columns:
            raise ValueError(
                f"Missing Gold feature: {column}"
            )

    if df.empty:
        raise ValueError(
            "Gold dataset is empty."
        )

    print("Gold validation passed!")


def load(df):

    print("Writing Gold data...")

    os.makedirs(
        "data/gold",
        exist_ok=True
    )

    df.to_csv(
        GOLD_FILE,
        index=False
    )

    print(
        f"Saved {len(df)} Gold records."
    )


def run_pipeline():

    df = extract_silver()

    df = create_features(df)

    validate(df)

    load(df)

    print(
        "Gold pipeline completed!"
    )


if __name__ == "__main__":
    run_pipeline()