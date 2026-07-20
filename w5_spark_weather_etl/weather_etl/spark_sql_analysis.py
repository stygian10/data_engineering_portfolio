"""
spark_sql_analysis.py

Week 5 - Spark SQL Analysis

Purpose:
1. Load the hourly Parquet dataset
2. Register a Spark SQL temporary view
3. Perform SQL analysis on hourly weather data
"""

import logging
from pathlib import Path

from pyspark.sql import SparkSession

# --------------------------------------------------
# CONFIGURE LOGGING
# --------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SparkSQLAnalysis")

# --------------------------------------------------
# INITIALIZE SPARK
# --------------------------------------------------
spark = (
    SparkSession.builder
    .appName("Week5_Spark_SQL_Analysis")
    .getOrCreate()
)

logger.info("Spark session started.")

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[1]

PARQUET_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "weather_week5.parquet"
)

# --------------------------------------------------
# LOAD PARQUET
# --------------------------------------------------
logger.info(f"Loading Parquet dataset from: {PARQUET_PATH}")

df = spark.read.parquet(str(PARQUET_PATH))

logger.info(f"Rows loaded: {df.count()}")

df.printSchema()
df.show(5)

# --------------------------------------------------
# REGISTER TEMP VIEW
# --------------------------------------------------
df.createOrReplaceTempView("weather_data")

logger.info("Temporary SQL view 'weather_data' registered.")

# ==================================================
# DATASET OVERVIEW
# ==================================================
logger.info("Dataset overview")

spark.sql("""
SELECT
    COUNT(*) AS total_rows
FROM weather_data
""").show()

# ==================================================
# RECORDS PER CITY
# ==================================================
logger.info("Records per city")

spark.sql("""
SELECT
    city,
    COUNT(*) AS total_records
FROM weather_data
GROUP BY city
ORDER BY city
""").show()

# ==================================================
# HISTORICAL VS FORECAST
# ==================================================
logger.info("Historical vs Forecast")

spark.sql("""
SELECT
    source,
    COUNT(*) AS total_records
FROM weather_data
GROUP BY source
ORDER BY source
""").show()

# ==================================================
# TEMPERATURE STATISTICS
# ==================================================
logger.info("Temperature statistics")

spark.sql("""
SELECT
    city,
    ROUND(AVG(temperature_2m),2) AS average_temperature,
    MAX(temperature_2m) AS highest_temperature,
    MIN(temperature_2m) AS lowest_temperature
FROM weather_data
GROUP BY city
ORDER BY city
""").show()

# ==================================================
# HUMIDITY STATISTICS
# ==================================================
logger.info("Humidity statistics")

spark.sql("""
SELECT
    city,
    ROUND(AVG(relative_humidity_2m),2) AS average_humidity
FROM weather_data
GROUP BY city
ORDER BY city
""").show()

# ==================================================
# WIND SPEED STATISTICS
# ==================================================
logger.info("Wind speed statistics")

spark.sql("""
SELECT
    city,
    ROUND(AVG(wind_speed_10m),2) AS average_wind_speed,
    MAX(wind_speed_10m) AS maximum_wind_speed
FROM weather_data
GROUP BY city
ORDER BY city
""").show()

# ==================================================
# TIME RANGE PER CITY
# ==================================================
logger.info("Time range per city")

spark.sql("""
SELECT
    city,
    MIN(time) AS first_record,
    MAX(time) AS latest_record
FROM weather_data
GROUP BY city
ORDER BY city
""").show(truncate=False)

# ==================================================
# LATEST FORECAST RECORDS
# ==================================================
logger.info("Latest forecast timestamp")

spark.sql("""
SELECT
    city,
    MAX(time) AS latest_forecast_time
FROM weather_data
WHERE source = 'forecast'
GROUP BY city
ORDER BY city
""").show(truncate=False)

# --------------------------------------------------
# SHUTDOWN
# --------------------------------------------------
spark.stop()

logger.info("Spark SQL analysis completed successfully.")