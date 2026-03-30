"""
spark_sql_analysis.py

Week 5 – Spark SQL Analysis Layer (Updated with City)
-----------------------------------------------------

Purpose:
1. Load transformed Parquet dataset from Week 5
2. Register Spark SQL temporary view
3. Run analytical queries per city:
   - Daily summary
   - Weekly summary
   - Temperature extremes
4. Validate results against combined Week 4 pandas CSV (if available)
"""

import os
import glob
import logging
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import weekofyear, year, col

# --------------------------------------------------
# CONFIGURE LOGGING
# --------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SparkSQLAnalysis")

# --------------------------------------------------
# INITIALIZE SPARK SESSION
# --------------------------------------------------
spark = SparkSession.builder \
    .appName("Week5_Spark_SQL_Analysis") \
    .getOrCreate()

logger.info("Spark session started.")

# --------------------------------------------------
# RESOLVE PROJECT PATHS
# --------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

# Week 5 Parquet output
parquet_path = os.path.join(
    project_root,
    "data",
    "processed",
    "weather_week5.parquet"
)

# Week 4 pandas processed folder (for optional validation)
week4_processed_folder = os.path.join(
    project_root,
    "..",
    "airflow_weather_pipeline",
    "data",
    "processed"
)

# --------------------------------------------------
# LOAD TRANSFORMED PARQUET DATA
# --------------------------------------------------
logger.info(f"Loading Parquet dataset from: {parquet_path}")
df_daily = spark.read.parquet(parquet_path)
df_daily.printSchema()
df_daily.show(5)

# --------------------------------------------------
# REGISTER TEMP VIEW
# --------------------------------------------------
df_daily.createOrReplaceTempView("daily_weather")
logger.info("Temporary SQL view 'daily_weather' registered.")

# ==================================================
# 1️⃣ DAILY SUMMARY PER CITY
# ==================================================
logger.info("Running daily summary query per city...")
daily_summary = spark.sql("""
    SELECT
        city,
        date,
        avg_temp,
        max_temp,
        min_temp,
        avg_humidity,
        avg_windspeed,
        rolling_avg_temp
    FROM daily_weather
    ORDER BY city, date
""")
daily_summary.show(10)

# ==================================================
# 2️⃣ WEEKLY SUMMARY PER CITY
# ==================================================
logger.info("Generating weekly summary with year included per city...")
df_with_week = df_daily.withColumn("year", year(col("date"))) \
                       .withColumn("week", weekofyear(col("date")))
df_with_week.createOrReplaceTempView("daily_weather_week")

weekly_summary = spark.sql("""
    SELECT
        city,
        year,
        week,
        ROUND(AVG(avg_temp), 2) AS weekly_avg_temp,
        ROUND(AVG(avg_humidity), 2) AS weekly_avg_humidity,
        ROUND(AVG(avg_windspeed), 2) AS weekly_avg_windspeed
    FROM daily_weather_week
    GROUP BY city, year, week
    ORDER BY city, year, week
""")
weekly_summary.show(10)

# ==================================================
# 3️⃣ TEMPERATURE EXTREMES PER CITY
# ==================================================
logger.info("Calculating temperature extremes per city...")
city_extremes = spark.sql("""
    SELECT
        city,
        MAX(max_temp) AS highest_recorded_temp,
        MIN(min_temp) AS lowest_recorded_temp
    FROM daily_weather
    GROUP BY city
""")
city_extremes.show()

# ==================================================
# 4️⃣ OPTIONAL VALIDATION AGAINST WEEK 4 CSVs (Robust)
# ==================================================
logger.info("Validating Spark results against Week 4 pandas outputs...")

csv_files = glob.glob(os.path.join(week4_processed_folder, "*_weather_daily.csv"))
logger.info(f"Found {len(csv_files)} Week 4 CSV files.")

if csv_files:
    pandas_df_list = [pd.read_csv(file) for file in csv_files]
    pandas_df = pd.concat(pandas_df_list, ignore_index=True)
    logger.info("Combined pandas DataFrame preview:")
    print(pandas_df.head())

    # Row Count Comparison
    spark_count = df_daily.count()
    pandas_count = len(pandas_df)
    logger.info(f"Row count comparison → Spark: {spark_count}, Pandas: {pandas_count}")
    if spark_count == pandas_count:
        logger.info("Row counts match.")
    else:
        logger.warning("Row counts DO NOT match.")

    # Extreme Value Validation (per city)
    if "city" in pandas_df.columns:
        pandas_extremes = pandas_df.groupby("city").agg({
            "max_temp": "max",
            "min_temp": "min"
        }).reset_index()

        spark_extremes_pd = city_extremes.toPandas()

        # Merge on city, keep all Spark cities
        comparison = pd.merge(
            spark_extremes_pd,
            pandas_extremes,
            on="city",
            how="left",
            suffixes=("_spark", "_pandas")
        )

        # Warn if any Spark city is missing in Week 4 CSVs
        missing_cities = comparison[comparison["max_temp_pandas"].isna()]["city"].tolist()
        if missing_cities:
            logger.warning(f"These cities are in Spark but missing in Week 4 CSVs: {missing_cities}")

        print("\nComparison of Spark vs Pandas Extremes (per city):")
        print(comparison.fillna("Missing"))
    else:
        logger.warning("Week 4 CSVs do not have 'city' column. Skipping per-city extremes validation.")
else:
    logger.info("No Week 4 CSV files found. Skipping validation.")

# ==================================================
# CLEAN SHUTDOWN 
# ==================================================
spark.stop()
logger.info("Spark SQL analysis completed successfully.")