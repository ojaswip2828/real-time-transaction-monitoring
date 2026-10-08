import json
from kafka import KafkaConsumer


KAFKA_SERVER = "localhost:9092"
TOPIC = "transactions"


def create_consumer():

    return KafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=lambda value: json.loads(
            value.decode("utf-8")
        ),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="transaction-monitoring-group"
    )


def consume_transactions():

    consumer = create_consumer()

    print("Kafka consumer started...")
    print("Waiting for transactions...")

    for message in consumer:

        transaction = message.value

        print(
            f"Received transaction: "
            f"{transaction['transaction_id']} | "
            f"Amount: {transaction['amount']}"
        )


if __name__ == "__main__":
    consume_transactions()