import json
import random
import os
from datetime import datetime, timedelta


NUM_TRANSACTIONS = 1000


locations = [
    "Bangalore",
    "Delhi",
    "Mumbai",
    "Hyderabad",
    "Chennai",
    "Pune",
    "London",
    "New York"
]


merchants = [
    "Amazon",
    "Flipkart",
    "Swiggy",
    "Zomato",
    "Uber",
    "Myntra",
    "Walmart",
    "Apple"
]


def generate_transaction(transaction_id):

    customer_id = f"C{random.randint(1000, 1100)}"

    amount = round(
        random.uniform(100, 10000),
        2
    )

    timestamp = (
        datetime.now()
        - timedelta(
            minutes=random.randint(0, 10080)
        )
    )

    transaction = {
        "transaction_id": transaction_id,
        "customer_id": customer_id,
        "amount": amount,
        "location": random.choice(locations),
        "timestamp": timestamp.isoformat(),
        "merchant": random.choice(merchants)
    }

    return transaction


def generate_data():

    transactions = []

    for i in range(1, NUM_TRANSACTIONS + 1):

        transaction = generate_transaction(i)

        transactions.append(transaction)

        # -------------------------
    # Add dirty data
    # -------------------------

    # Duplicate transaction
    transactions.append(
        transactions[0].copy()
    )

    # Missing customer ID
    transactions.append({
        "transaction_id": 2001,
        "customer_id": None,
        "amount": 2500,
        "location": "Bangalore",
        "timestamp": datetime.now().isoformat(),
        "merchant": "Amazon"
    })

    # Missing amount
    transactions.append({
        "transaction_id": 2002,
        "customer_id": "C1050",
        "amount": None,
        "location": "Delhi",
        "timestamp": datetime.now().isoformat(),
        "merchant": "Flipkart"
    })

    # Invalid negative amount
    transactions.append({
        "transaction_id": 2003,
        "customer_id": "C1051",
        "amount": -500,
        "location": "Mumbai",
        "timestamp": datetime.now().isoformat(),
        "merchant": "Uber"
    })

    # Invalid timestamp
    transactions.append({
        "transaction_id": 2004,
        "customer_id": "C1052",
        "amount": 3000,
        "location": "Chennai",
        "timestamp": "INVALID_TIMESTAMP",
        "merchant": "Zomato"
    })


    # Add suspicious transaction
    transactions.append({
        "transaction_id": 1001,
        "customer_id": "C1001",
        "amount": 500000,
        "location": "London",
        "timestamp": datetime.now().isoformat(),
        "merchant": "Apple"
    })


    # Add another suspicious transaction
    transactions.append({
        "transaction_id": 1002,
        "customer_id": "C1002",
        "amount": 750000,
        "location": "New York",
        "timestamp": datetime.now().isoformat(),
        "merchant": "Walmart"
    })


    # Create data/raw directory
    os.makedirs(
        "data/raw",
        exist_ok=True
    )


    # Save JSON
    with open(
        "data/raw/transactions.json",
        "w"
    ) as file:

        json.dump(
            transactions,
            file,
            indent=4
        )


    print(
        f"Generated {len(transactions)} transactions."
    )


if __name__ == "__main__":
    generate_data()