from pathlib import Path
import os

# Project Paths

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

RAW_DATA_FILE = RAW_DATA_DIR / "historical_weather.csv"
PROCESSED_DATA_FILE = PROCESSED_DATA_DIR / "uk_weather_clean.csv"

# Open-Meteo Configuration

API_URL = os.getenv(
    "OPEN_METEO_ARCHIVE_URL",
    "https://archive-api.open-meteo.com/v1/archive",
)

TIMEZONE = os.getenv(
    "TIMEZONE",
    "UTC",
)

START_DATE = os.getenv(
    "W1_START_DATE",
    "2025-01-01",
)

# End date will always be calculated in download.py as yesterday.

# Cities

CITIES = [
    {
        "name": "London",
        "latitude": 51.5074,
        "longitude": -0.1278,
    },
    {
        "name": "Manchester",
        "latitude": 53.4808,
        "longitude": -2.2426,
    },
    {
        "name": "Edinburgh",
        "latitude": 55.9533,
        "longitude": -3.1883,
    },
]

# Weather Variables

HOURLY_VARIABLES = os.getenv(
    "HOURLY_VARIABLES",
    "temperature_2m,relative_humidity_2m,wind_speed_10m",
).split(",")

# Request Configuration

REQUEST_TIMEOUT = int(
    os.getenv("REQUEST_TIMEOUT", "60")
)