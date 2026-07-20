from weather_etl.config import PARQUET_PATH


def save_parquet(df):
    """
    Save the transformed Spark DataFrame
    as a Parquet dataset.
    """

    df.write.mode("overwrite").parquet(
        str(PARQUET_PATH)
    )

    print(f"[LOAD] Parquet saved to: {PARQUET_PATH}")
    print(f"[LOAD] Rows written: {df.count()}")