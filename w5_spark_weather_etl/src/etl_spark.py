from pyspark.sql import SparkSession
from pyspark.sql.functions import col, input_file_name, regexp_extract
from pathlib import Path

# ---------------- Paths ----------------
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent

RAW_PATH = PROJECT_ROOT / "data" / "raw"
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"

# ---------------- Initialize Spark ----------------
spark = SparkSession.builder.appName("Week5_Weather_ETL").getOrCreate()

# ---------------- EXTRACT ----------------
# Load all CSV files from the raw folder and add a column with the file path
raw_df = spark.read.option("header", True).csv(str(RAW_PATH / "*.csv")) \
    .withColumn("source_file", input_file_name())  # adds full file path

# Extract city name from filename, assuming files like "edinburgh.csv", "london.csv"
raw_df = raw_df.withColumn("city", regexp_extract(col("source_file"), r'([^/]+)\.csv$', 1))

print("Schema with city column:")
raw_df.printSchema()
raw_df.show(5)

# ---------------- TRANSFORM ----------------
# Rename & select only needed columns + city
clean_df = raw_df.select(
    col("city"),
    col("time").alias("date"),
    col("temperature_2m").alias("temp_mean"),
    col("relativehumidity_2m").alias("humidity"),
    col("windspeed_10m").alias("wind_speed")
)

# Cast columns to float
clean_df = clean_df.withColumn("temp_mean", col("temp_mean").cast("float")) \
                   .withColumn("humidity", col("humidity").cast("float")) \
                   .withColumn("wind_speed", col("wind_speed").cast("float"))

# Drop rows with nulls
clean_df = clean_df.dropna()

# ---------------- LOAD ----------------
output_path = PROCESSED_PATH / "weather_cleaned"
clean_df.write.mode("overwrite").option("header", True).csv(str(output_path))
print("Processed CSV saved at:", output_path)

# ---------------- Stop Spark ----------------
spark.stop()
