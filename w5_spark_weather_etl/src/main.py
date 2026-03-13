from pathlib import Path
from pyspark.sql import SparkSession
import glob
import pandas as pd

from transform import clean_data, aggregate_daily, add_rolling_avg
from load import save_parquet

# ---------------- Paths ----------------
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent

RAW_PATH = PROJECT_ROOT / "data" / "raw"
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"

# Week 4 processed CSV folder
WEEK4_PROCESSED = PROJECT_ROOT.parent / "airflow_weather_pipeline" / "data" / "processed"

# Ensure folders exist
RAW_PATH.mkdir(parents=True, exist_ok=True)
PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

# ---------------- Combine Week 4 CSVs with city column ----------------
combined_csv_path = RAW_PATH / "combined_week4.csv"
csv_files = glob.glob(str(WEEK4_PROCESSED / "*.csv"))

if not csv_files:
    raise FileNotFoundError(f"No CSV files found in {WEEK4_PROCESSED}")

df_list = []
for f in csv_files:
    # Extract city name from filename
    # Filename pattern: weather_processed_<City>_<YYYYMMDD>_<HHMMSS>.csv
    city_name = Path(f).stem.split("_")[2].capitalize()
    temp_df = pd.read_csv(f)
    temp_df['city'] = city_name  # Add city column
    df_list.append(temp_df)

combined_df = pd.concat(df_list, ignore_index=True)
combined_df.to_csv(combined_csv_path, index=False)
print(f"Combined CSV with city column saved to: {combined_csv_path}")

# ---------------- Start Spark ----------------
spark = SparkSession.builder.appName("Week5_Weather_ETL").getOrCreate()

# ---------------- Load CSV into Spark ----------------
df_raw = spark.read.csv(str(combined_csv_path), header=True, inferSchema=True)

# ---------------- Transform ----------------
df_clean = clean_data(df_raw)            # cleans data and creates 'date' column
df_daily = aggregate_daily(df_clean)     # aggregates daily averages per city
df_final = add_rolling_avg(df_daily)     # adds rolling average per city

# ---------------- Save Parquet ----------------
save_parquet(df_final, str(PROCESSED_PATH), folder_name="weather_week5.parquet")

# ---------------- Stop Spark ----------------
spark.stop()
print("Week 5 ETL completed successfully with city column.")
