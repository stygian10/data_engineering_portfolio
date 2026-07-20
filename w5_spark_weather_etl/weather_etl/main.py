from pyspark.sql import SparkSession

from weather_etl.config import SPARK_APP_NAME
from weather_etl.extract import extract_data
from weather_etl.transform import transform_data
from weather_etl.load import save_parquet


def main():
    """
    Week 5 Spark ETL Pipeline

    PostgreSQL
        ↓
    Extract
        ↓
    Raw CSV
        ↓
    Spark Transform
        ↓
    Hourly Parquet
    """

    spark = (
        SparkSession.builder
        .appName(SPARK_APP_NAME)
        .config(
            "spark.jars",
            "/opt/spark/jars/postgresql-42.7.7.jar"
        )
        .getOrCreate()
    )

    try:
        print("[START] Week 5 Spark ETL")

        # Extract
        df = extract_data(spark)

        # Transform
        df = transform_data(df)

        # Load
        save_parquet(df)

        print("[SUCCESS] Week 5 ETL completed successfully.")

    finally:
        spark.stop()


if __name__ == "__main__":
    main()