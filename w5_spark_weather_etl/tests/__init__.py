from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pathlib import Path

# Resolve project paths dynamically
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent

RAW_PATH = PROJECT_ROOT / "data" / "raw"
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"

# Initialize Spark
spark = SparkSession.builder \
    .appName("Week5_Weather_ETL") \
    .getOrCreate()

# Load ALL raw CSV files dynamically
raw_df = spark.read.csv(
    str(RAW_PATH / "*.csv"),
    header=True,
    inferSchema=True
)

print("Schema of raw data:")
raw_df.printSchema()
raw_df.show(5)

# Basic cleaning
clean_df = raw_df.dropna()

if "temperature_2m_mean" in clean_df.columns:
    clean_df = clean_df.withColumn(
        "temperature_2m_mean",
        col("temperature_2m_mean").cast("float")
    )

if "precipitation_sum" in clean_df.columns:
    clean_df = clean_df.withColumn(
        "precipitation_sum",
        col("precipitation_sum").cast("float")
    )

# Save processed output
clean_df.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv(str(PROCESSED_PATH / "weather_cleaned"))

print("Processed CSV saved at:", PROCESSED_PATH / "weather_cleaned")

spark.stop()
