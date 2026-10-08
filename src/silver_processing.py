import json
import pandas as pd
import os


BRONZE_FILE = "data/bronze/transactions.jsonl"
SILVER_FILE = "data/silver/clean_transactions.csv"


def extract_bronze():

    print("Reading Bronze data...")

    transactions = []

    with open(BRONZE_FILE, "r") as file:

        for line in file:
            transactions.append(json.loads(line))

    df = pd.DataFrame(transactions)

    print(f"Read {len(df)} Bronze records.")

    return df


def transform(df):

    print("Cleaning Bronze data...")

    # Remove duplicate transaction IDs
    before = len(df)

    df = df.drop_duplicates(
        subset=["transaction_id"]
    )

    print(
        f"Removed {before - len(df)} duplicate(s)."
    )

    # Convert amount to numeric
    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    # Remove invalid amounts
    invalid_amounts = (
        df["amount"].isna()
        | (df["amount"] <= 0)
    )

    print(
        f"Invalid amounts: "
        f"{invalid_amounts.sum()}"
    )

    df = df[~invalid_amounts]

    # Remove missing customer IDs
    missing_customers = df["customer_id"].isna().sum()

    print(
        f"Missing customer IDs: "
        f"{missing_customers}"
    )

    df = df.dropna(
        subset=["customer_id"]
    )

    # Convert timestamps
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

    # Remove invalid timestamps
    invalid_timestamps = df["timestamp"].isna()

    print(
        f"Invalid timestamps: "
        f"{invalid_timestamps.sum()}"
    )

    df = df.dropna(
        subset=["timestamp"]
    )

    # Create useful features
    df["date"] = df["timestamp"].dt.date

    df["hour"] = df["timestamp"].dt.hour

    df["is_high_value"] = (
        df["amount"] > 10000
    )

    return df


def validate(df):

    print("Validating Silver data...")

    if df.empty:
        raise ValueError(
            "Silver dataset is empty."
        )

    if df["transaction_id"].duplicated().any():
        raise ValueError(
            "Duplicate transaction IDs found."
        )

    if df["customer_id"].isna().any():
        raise ValueError(
            "Missing customer IDs found."
        )

    if (df["amount"] <= 0).any():
        raise ValueError(
            "Invalid transaction amounts found."
        )

    if df["timestamp"].isna().any():
        raise ValueError(
            "Invalid timestamps found."
        )

    print("Silver validation passed!")


def load(df):

    print("Writing Silver data...")

    os.makedirs(
        "data/silver",
        exist_ok=True
    )

    df.to_csv(
        SILVER_FILE,
        index=False
    )

    print(
        f"Saved {len(df)} Silver records."
    )


def run_pipeline():

    df = extract_bronze()

    df = transform(df)

    validate(df)

    load(df)

    print(
        "Silver pipeline completed!"
    )


if __name__ == "__main__":
    run_pipeline()