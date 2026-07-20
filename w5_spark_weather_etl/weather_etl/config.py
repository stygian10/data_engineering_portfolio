from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

SPARK_APP_NAME = "Week5_Spark_Weather_ETL"

TABLE_NAME = "weather_data"

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "airflow")
DB_USER = os.getenv("DB_USER", "airflow")
DB_PASSWORD = os.getenv("DB_PASSWORD", "airflow")

JDBC_URL = (
    f"jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

JDBC_DRIVER = "org.postgresql.Driver"

RAW_CSV_NAME = "weather_data.csv"

PARQUET_NAME = "weather_week5.parquet"

RAW_CSV_PATH = RAW_DATA_DIR / RAW_CSV_NAME

PARQUET_PATH = PROCESSED_DATA_DIR / PARQUET_NAME