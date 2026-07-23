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
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

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
HOURLY_VARIABLES = [
    "temperature_2m",
    "relative_humidity_2m",
    "windspeed_10m",
]

TIMEZONE = "UTC"

# PostgreSQL Configuration
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "airflow")
DB_USER = os.getenv("DB_USER", "airflow")
DB_PASSWORD = os.getenv("DB_PASSWORD", "airflow")

TABLE_NAME = "weather_data"