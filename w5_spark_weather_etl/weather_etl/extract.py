from pyspark.sql import DataFrame

from weather_etl.config import (
    JDBC_URL,
    JDBC_DRIVER,
    DB_USER,
    DB_PASSWORD,
    TABLE_NAME,
    RAW_CSV_PATH,
)


def extract_data(spark) -> DataFrame:
    """
    Extract weather data from PostgreSQL using Spark JDBC,
    save a raw CSV snapshot,
    and return a Spark DataFrame.
    """

    spark_df = (
        spark.read
        .format("jdbc")
        .option("url", JDBC_URL)
        .option("dbtable", TABLE_NAME)
        .option("user", DB_USER)
        .option("password", DB_PASSWORD)
        .option("driver", JDBC_DRIVER)
        .load()
    )

    if spark_df.count() == 0:
        raise ValueError("No data found in PostgreSQL.")

    spark_df.write.mode("overwrite").option("header", True).csv(
        str(RAW_CSV_PATH)
    )

    print(f"[EXTRACT] Rows extracted: {spark_df.count()}")
    print(f"[EXTRACT] Raw data saved to: {RAW_CSV_PATH}")

    return spark_df