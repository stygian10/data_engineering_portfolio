# test_pyspark_vs_pandas_real_fixed.py
import os
import sys
import pandas as pd
import numpy as np
from pyspark.sql import SparkSession

# ---------------- Paths ----------------
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
sys.path.insert(0, SRC_PATH)
RAW_CSV_PATH = os.path.join(PROJECT_ROOT, "..", "data", "raw", "combined_week4.csv")  # Week 4 combined CSV

# ---------------- Initialize Spark ----------------
spark = SparkSession.builder.appName("PySpark_vs_Pandas_MaxMin").getOrCreate()

# ---------------- 1️⃣ Load CSV in PySpark ----------------
df_spark = spark.read.csv(RAW_CSV_PATH, header=True, inferSchema=True)
print("Raw PySpark Data Preview:")
df_spark.show(5)

# ---------------- 2️⃣ PySpark ETL ----------------
df_clean_spark = clean_data(df_spark)
df_daily_spark = aggregate_daily(df_clean_spark)
df_daily_spark = df_daily_spark.select("city", "date", "max_temp", "min_temp")
print("\nPySpark Daily Aggregation (max/min temp):")
df_daily_spark.show(5)

# Convert to Pandas
df_daily_spark_pd = df_daily_spark.toPandas()

# ---------------- 3️⃣ Pandas ETL ----------------
df_pandas = pd.read_csv(RAW_CSV_PATH, parse_dates=["time"])
df_pandas = df_pandas.dropna(subset=["temperature_2m"])

# Aggregate daily per city
daily_pandas = df_pandas.groupby([df_pandas['city'], df_pandas['time'].dt.date]).agg(
    max_temp=("temperature_2m", "max"),
    min_temp=("temperature_2m", "min")
).reset_index()

# Rename for consistency
daily_pandas.rename(columns={'time': 'date'}, inplace=True)
daily_pandas['date'] = pd.to_datetime(daily_pandas['time'], errors='coerce')  # safe conversion
daily_pandas['date'] = pd.to_datetime(daily_pandas['date'].fillna(pd.NaT))  # ensure no NaT

# ---------------- 4️⃣ Merge for Comparison ----------------
comparison = pd.merge(
    df_daily_spark_pd,
    daily_pandas,
    on=["city", "date"],
    suffixes=('_spark', '_pandas')
)

print("\nComparison (PySpark vs Pandas) Max/Min Temperature:")
print(comparison.head(10))

# ---------------- 5️⃣ Optional: Check for mismatch ----------------
mismatch = comparison[(comparison['max_temp_spark'] != comparison['max_temp_pandas']) |
                      (comparison['min_temp_spark'] != comparison['min_temp_pandas'])]
if mismatch.empty:
    print("\n✅ All max/min temperatures match between PySpark and Pandas!")
else:
    print("\n⚠️ Mismatches found:")
    print(mismatch)

# ---------------- Stop Spark ----------------
spark.stop()
