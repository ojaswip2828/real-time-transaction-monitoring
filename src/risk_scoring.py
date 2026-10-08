import pandas as pd
import os

INPUT_FILE = "data/gold/anomaly_results.csv"
OUTPUT_FILE = "data/gold/final_anomaly_results.csv"


def load_data():
    print("Loading anomaly results...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Loaded {len(df)} transactions.")

    return df


def calculate_risk_score(df):
    print("Calculating risk scores...")

    # Convert Isolation Forest score into a simple 0-100 risk score.
    # Lower anomaly scores indicate more unusual transactions.
    min_score = df["anomaly_score"].min()
    max_score = df["anomaly_score"].max()

    df["risk_score"] = (
        (max_score - df["anomaly_score"])
        / (max_score - min_score)
        * 100
    )

    df["risk_score"] = df["risk_score"].round(2)

    return df


def assign_risk_level(df):
    print("Assigning risk levels...")

    def classify(score):
        if score >= 90:
            return "CRITICAL"
        elif score >= 70:
            return "HIGH"
        elif score >= 40:
            return "MEDIUM"
        else:
            return "LOW"

    df["risk_level"] = df["risk_score"].apply(classify)

    return df


def save_results(df):
    print("Saving final anomaly results...")

    os.makedirs("data/gold", exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved results to: {OUTPUT_FILE}")


def show_risky_transactions(df):

    print("\n===== HIGH RISK TRANSACTIONS =====")

    risky = (
        df[df["risk_level"].isin(["HIGH", "CRITICAL"])]
        .sort_values("risk_score", ascending=False)
    )

    columns = [
        "transaction_id",
        "customer_id",
        "amount",
        "anomaly_score",
        "risk_score",
        "risk_level",
        "anomaly_prediction"
    ]

    print(risky[columns].head(20).to_string(index=False))


def main():

    df = load_data()

    df = calculate_risk_score(df)

    df = assign_risk_level(df)

    show_risky_transactions(df)

    save_results(df)

    print("\nRisk scoring completed.")


if __name__ == "__main__":
    main()