from pyspark.sql import functions as F
from pyspark.sql.window import Window

def clean_data(df):
    df = df.dropna(subset=[
        "temperature_2m",
        "relativehumidity_2m",
        "windspeed_10m"
    ])

    df = df.withColumn("date", F.to_date("time", "yyyy-MM-dd"))

    return df


def aggregate_daily(df):
    return df.groupBy("city", "date").agg(
        F.round(F.avg("temperature_2m"), 2).alias("avg_temp"),
        F.round(F.max("temperature_2m"), 2).alias("max_temp"),
        F.round(F.min("temperature_2m"), 2).alias("min_temp"),
        F.round(F.avg("relativehumidity_2m"), 2).alias("avg_humidity"),
        F.round(F.avg("windspeed_10m"), 2).alias("avg_windspeed")
    )


def add_rolling_avg(df, window_size=3):
    window = Window.partitionBy("city").orderBy("date").rowsBetween(-(window_size - 1), 0)

    return df.withColumn(
        "rolling_avg_temp",
        F.round(F.avg("avg_temp").over(window), 2)
    )