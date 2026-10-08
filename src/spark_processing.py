from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    avg,
    max,
    count,
    when
)


SILVER_FILE = "data/silver/clean_transactions.csv"
SPARK_OUTPUT = "data/gold/spark_transactions"


def create_spark_session():

    spark = (
        SparkSession
        .builder
        .appName("TransactionMonitoring")
        .master("local[*]")
        .getOrCreate()
    )

    return spark


def main():

    spark = create_spark_session()

    print("Spark started.")

    # Read Silver data
    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(SILVER_FILE)
    )

    print("Silver data loaded.")

    print(f"Total records: {df.count()}")

    # Show schema
    df.printSchema()

    # Customer-level statistics
    customer_stats = (
        df.groupBy("customer_id")
        .agg(
            avg("amount").alias("customer_avg_amount"),
            max("amount").alias("customer_max_amount"),
            count("transaction_id").alias(
                "customer_transaction_count"
            )
        )
    )

    # Join statistics back to transactions
    result = df.join(
        customer_stats,
        on="customer_id",
        how="left"
    )

    # Create anomaly-related features
    result = result.withColumn(
        "amount_vs_customer_avg",
        col("amount") /
        col("customer_avg_amount")
    )

    result = result.withColumn(
        "is_high_value",
        when(
            col("amount") > 10000,
            True
        ).otherwise(False)
    )

    print("Spark transformations completed.")

    result.show(10, truncate=False)

    # Save Spark output
    (
        result.write
        .mode("overwrite")
        .option("header", True)
        .csv(SPARK_OUTPUT)
    )

    print(
        f"Spark output saved to: {SPARK_OUTPUT}"
    )

    spark.stop()

    print("Spark job completed.")


if __name__ == "__main__":
    main()