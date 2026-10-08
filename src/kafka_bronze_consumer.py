import json
import os

from kafka import KafkaConsumer


KAFKA_SERVER = "localhost:9092"
TOPIC = "transactions"

BRONZE_FILE = "data/bronze/transactions.jsonl"


def create_consumer():

    return KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=lambda value: json.loads(
            value.decode("utf-8")
        ),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="bronze-storage-group-v3"
    )


def store_transactions():

    os.makedirs("data/bronze", exist_ok=True)

    consumer = create_consumer()

    print("Bronze consumer started...")
    print("Waiting for new transactions...")

    with open(BRONZE_FILE, "w") as file:

        for message in consumer:

            transaction = message.value

            file.write(
                json.dumps(transaction) + "\n"
            )

            file.flush()

            print(
                f"Stored transaction: "
                f"{transaction['transaction_id']}"
            )


if __name__ == "__main__":
    store_transactions()