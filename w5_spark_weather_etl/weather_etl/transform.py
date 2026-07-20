from pyspark.sql import functions as F


def clean_data(df):
    """
    Clean and standardize the weather dataset.
    """

    df = df.dropna(
        subset=[
            "time",
            "city",
            "temperature_2m",
            "relative_humidity_2m",
            "wind_speed_10m",
            "source",
        ]
    )

    df = df.withColumn(
        "time",
        F.to_timestamp("time")
    )

    df = df.withColumn(
        "date",
        F.to_date("time")
    )

    return df


def transform_data(df):
    """
    Apply Spark transformations while preserving
    hourly weather observations.
    """

    df = clean_data(df)

    df = df.orderBy(
        "city",
        "time"
    )

    return df