import streamlit as st
import requests
import pandas as pd


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Transaction Monitoring",
    page_icon="🚨",
    layout="wide"
)


st.title("🏦 Real-Time Transaction Monitoring")
st.caption("Banking transaction anomaly detection dashboard")


# --------------------------------------------------
# Get statistics
# --------------------------------------------------

try:

    stats_response = requests.get(
        f"{API_URL}/stats",
        timeout=5
    )

    stats_response.raise_for_status()

    stats = stats_response.json()

except requests.exceptions.RequestException:

    st.error(
        "Could not connect to FastAPI. "
        "Make sure the API server is running."
    )

    st.stop()


# --------------------------------------------------
# Metrics
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Transactions",
    stats["total_transactions"]
)

col2.metric(
    "Anomalies",
    stats["total_anomalies"]
)

col3.metric(
    "Critical",
    stats["critical_transactions"]
)

col4.metric(
    "High Risk",
    stats["high_risk_transactions"]
)


st.divider()


# --------------------------------------------------
# Risk Distribution
# --------------------------------------------------

st.subheader("Risk Distribution")

risk_data = pd.DataFrame(
    {
        "Risk Level": [
            "CRITICAL",
            "HIGH",
            "MEDIUM",
            "LOW"
        ],
        "Count": [
            stats["critical_transactions"],
            stats["high_risk_transactions"],
            stats["medium_risk_transactions"],
            stats["low_risk_transactions"]
        ]
    }
)

st.bar_chart(
    risk_data.set_index("Risk Level")
)


st.divider()


# --------------------------------------------------
# Anomalies
# --------------------------------------------------

st.subheader("🚨 Detected Anomalies")

try:

    anomaly_response = requests.get(
        f"{API_URL}/anomalies",
        timeout=5
    )

    anomaly_response.raise_for_status()

    anomaly_data = anomaly_response.json()

    anomalies = pd.DataFrame(
        anomaly_data["anomalies"]
    )

    if not anomalies.empty:

        columns = [
            "transaction_id",
            "customer_id",
            "amount",
            "anomaly_score",
            "risk_score",
            "risk_level"
        ]

        available_columns = [
            col for col in columns
            if col in anomalies.columns
        ]

        st.dataframe(
            anomalies[available_columns],
            use_container_width=True
        )

    else:

        st.success("No anomalies detected.")

except requests.exceptions.RequestException:

    st.error("Could not retrieve anomaly data.")


st.divider()


# --------------------------------------------------
# Transaction Lookup
# --------------------------------------------------

st.subheader("🔎 Transaction Lookup")

transaction_id = st.number_input(
    "Enter Transaction ID",
    min_value=1,
    step=1
)


if st.button("Search Transaction"):

    try:

        response = requests.get(
            f"{API_URL}/transactions/{transaction_id}",
            timeout=5
        )

        if response.status_code == 404:

            st.warning("Transaction not found.")

        else:

            response.raise_for_status()

            transaction = response.json()

            st.json(transaction)

    except requests.exceptions.RequestException:

        st.error("Could not connect to the API.")