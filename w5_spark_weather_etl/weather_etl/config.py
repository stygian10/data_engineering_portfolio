from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

SPARK_APP_NAME = os.getenv(
    "SPARK_APP_NAME",
    "Week5_Spark_Weather_ETL",
)

SPARK_POSTGRES_JAR = os.getenv(
    "SPARK_POSTGRES_JAR",
    "/opt/spark/jars/postgresql-42.7.7.jar",
)

TABLE_NAME = os.getenv(
    "DB_TABLE_NAME",
    "weather_data",
)

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "airflow")
POSTGRES_USER = os.getenv("POSTGRES_USER", "airflow")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "airflow")

JDBC_URL = (
    f"jdbc:postgresql://{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

JDBC_DRIVER = os.getenv(
    "JDBC_DRIVER",
    "org.postgresql.Driver",
)

RAW_CSV_NAME = "weather_data.csv"
PARQUET_NAME = "weather_week5.parquet"

RAW_CSV_PATH = RAW_DATA_DIR / RAW_CSV_NAME
PARQUET_PATH = PROCESSED_DATA_DIR / PARQUET_NAME