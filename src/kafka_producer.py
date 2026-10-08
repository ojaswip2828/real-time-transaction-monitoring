import json
import time
from kafka import KafkaProducer


KAFKA_SERVER = "localhost:9092"
TOPIC = "transactions"
RAW_FILE = "data/raw/transactions.json"


def create_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        value_serializer=lambda value: json.dumps(value).encode("utf-8")
    )


def send_transactions():

    producer = create_producer()

    print("Starting Kafka producer...")

    with open(RAW_FILE, "r") as file:
        transactions = json.load(file)

    for transaction in transactions:

        producer.send(
            TOPIC,
            value=transaction
        )

        print(
            f"Sent transaction: "
            f"{transaction['transaction_id']}"
        )

        time.sleep(0.1)

    producer.flush()

    print("All transactions sent successfully.")

    producer.close()


if __name__ == "__main__":
    send_transactions()