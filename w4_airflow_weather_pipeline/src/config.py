from pathlib import Path
import os

# Base Project Directory
BASE_DIR = Path(__file__).resolve().parents[1]

# Data Directories
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
PARQUET_DATA_DIR = DATA_DIR / "parquet"

# Create directories if they do not exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
PARQUET_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Open-Meteo API
OPEN_METEO_URL = os.getenv(
    "OPEN_METEO_FORECAST_URL",
    "https://api.open-meteo.com/v1/forecast",
)

TIMEZONE = os.getenv("TIMEZONE", "UTC")

REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))

# Cities
CITIES = {
    "London": {
        "latitude": 51.5072,
        "longitude": -0.1276,
    },
    "Manchester": {
        "latitude": 53.4808,
        "longitude": -2.2426,
    },
    "Edinburgh": {
        "latitude": 55.9533,
        "longitude": -3.1883,
    },
}

# Weather Variables
HOURLY_VARIABLES = os.getenv(
    "HOURLY_VARIABLES",
    "temperature_2m,relative_humidity_2m,windspeed_10m",
).split(",")

# PostgreSQL Configuration
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "airflow")
POSTGRES_USER = os.getenv("POSTGRES_USER", "airflow")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "airflow")

# Database Table
TABLE_NAME = os.getenv("DB_TABLE_NAME", "weather_data")

# Project Directories
W1_DIR = Path( os.getenv("W1_DIR", "/opt/airflow/w1"))
W2_DIR = Path(os.getenv("W2_DIR", "/opt/airflow/w2"))
W3_DIR = Path(os.getenv("W3_DIR", "/opt/airflow/w3"))
HISTORICAL_DATASET = Path(os.getenv("HISTORICAL_DATASET",str(W2_DIR / "data" / "processed"),))