import pandas as pd
import os
import json


RAW_FILE = "data/raw/transactions.json"
PROCESSED_FILE = "data/processed/clean_transactions.csv"

def extract():

    print("Extracting data...")

    with open(RAW_FILE, "r") as file:
        data = json.load(file)

    df = pd.DataFrame(data)

    print(f"Extracted {len(df)} transactions.")

    return df

def transform(df):

    print("Transforming data...")

    # -------------------------
    # 1. Remove duplicates
    # -------------------------

    before = len(df)

    df = df.drop_duplicates(
        subset=["transaction_id"]
    )

    duplicates_removed = before - len(df)

    print(
        f"Removed {duplicates_removed} duplicate(s)."
    )


    # -------------------------
    # 2. Convert amount to numeric
    # -------------------------

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )


    # -------------------------
    # 3. Remove invalid amounts
    # -------------------------

    invalid_amounts = (
        df["amount"].isna()
        | (df["amount"] <= 0)
    )

    print(
        f"Invalid amounts found: "
        f"{invalid_amounts.sum()}"
    )

    df = df[~invalid_amounts]


    # -------------------------
    # 4. Handle missing customer IDs
    # -------------------------

    missing_customers = df["customer_id"].isna().sum()

    print(
        f"Missing customer IDs: "
        f"{missing_customers}"
    )

    df = df.dropna(
        subset=["customer_id"]
    )


    # -------------------------
    # 5. Convert timestamp
    # -------------------------

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )


    # -------------------------
    # 6. Remove invalid timestamps
    # -------------------------

    invalid_timestamps = (
        df["timestamp"].isna()
    )

    print(
        f"Invalid timestamps: "
        f"{invalid_timestamps.sum()}"
    )

    df = df.dropna(
        subset=["timestamp"]
    )


    # -------------------------
    # 7. Create date feature
    # -------------------------

    df["date"] = (
        df["timestamp"].dt.date
    )


    # -------------------------
    # 8. Create hour feature
    # -------------------------

    df["hour"] = (
        df["timestamp"].dt.hour
    )


    # -------------------------
    # 9. Create high-value flag
    # -------------------------

    df["is_high_value"] = (
        df["amount"] > 10000
    )


    return df
def validate(df):

    print("Validating data...")

    # 1. Check dataset is not empty
    if df.empty:
        raise ValueError("Validation failed: dataset is empty.")

    # 2. Check required columns
    required_columns = [
        "transaction_id",
        "customer_id",
        "amount",
        "location",
        "timestamp",
        "merchant"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Validation failed: missing columns {missing_columns}"
        )

    # 3. Check duplicate transaction IDs
    duplicate_count = df["transaction_id"].duplicated().sum()

    if duplicate_count > 0:
        raise ValueError(
            f"Validation failed: {duplicate_count} duplicate transaction IDs."
        )

    # 4. Check missing customer IDs
    missing_customers = df["customer_id"].isna().sum()

    if missing_customers > 0:
        raise ValueError(
            f"Validation failed: {missing_customers} missing customer IDs."
        )

    # 5. Check transaction amounts
    invalid_amounts = (df["amount"] <= 0).sum()

    if invalid_amounts > 0:
        raise ValueError(
            f"Validation failed: {invalid_amounts} invalid transaction amounts."
        )

    # 6. Check timestamps
    invalid_timestamps = df["timestamp"].isna().sum()

    if invalid_timestamps > 0:
        raise ValueError(
            f"Validation failed: {invalid_timestamps} invalid timestamps."
        )

    print("Data validation passed!")

def load(df):

    print("Loading data...")

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    df.to_csv(
        PROCESSED_FILE,
        index=False
    )

    print(
        f"Saved {len(df)} transactions."
    )


def run_pipeline():

    df = extract()

    df = transform(df)
    validate(df)

    load(df)

    print("ETL pipeline completed!")


if __name__ == "__main__":
    run_pipeline()