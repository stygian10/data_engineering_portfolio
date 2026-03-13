
from pyspark.sql.functions import col, avg, max, min, to_date, round as spark_round
from pyspark.sql.window import Window

def clean_data(df):
    """
    Clean raw weather data:
    - Drop rows with nulls in critical columns
    - Cast numeric columns explicitly
    - Create proper date column from 'time'
    """
    required_cols = ["time", "temperature_2m", "relativehumidity_2m", "windspeed_10m", "extraction_time", "city"]
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    df = df.dropna(subset=["temperature_2m", "relativehumidity_2m", "windspeed_10m"])

    df = df.withColumn("temperature_2m", col("temperature_2m").cast("float"))
    df = df.withColumn("relativehumidity_2m", col("relativehumidity_2m").cast("float"))
    df = df.withColumn("windspeed_10m", col("windspeed_10m").cast("float"))

    df = df.withColumn("date", to_date(col("time"), "yyyy-MM-dd"))

    return df

def aggregate_daily(df):
    """
    Aggregate weather data daily per city:
    - Compute avg, max, min temperature
    - Compute avg humidity and windspeed
    - Round numeric outputs to 2 decimals
    """
    daily_df = df.groupBy("city", "date").agg(
        spark_round(avg("temperature_2m"), 2).alias("avg_temp"),
        spark_round(max("temperature_2m"), 2).alias("max_temp"),
        spark_round(min("temperature_2m"), 2).alias("min_temp"),
        spark_round(avg("relativehumidity_2m"), 2).alias("avg_humidity"),
        spark_round(avg("windspeed_10m"), 2).alias("avg_windspeed")
    )
    return daily_df

def add_rolling_avg(df, window_size=3):
    """
    Add rolling average of avg_temp per city.
    Default window: 3 days including current row.
    """
    window_spec = Window.partitionBy("city").orderBy("date").rowsBetween(-(window_size - 1), 0)
    df = df.withColumn("rolling_avg_temp", spark_round(avg(col("avg_temp")).over(window_spec), 2))
    return df
