from pathlib import Path
from dotenv import load_dotenv
import os

# Project root

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")

# Week 6 project directory

PROJECT_DIR = Path(__file__).resolve().parents[1]

# MinIO Configuration

MINIO_ENDPOINT = os.getenv(
    "MINIO_ENDPOINT",
    "localhost:9000",
)

MINIO_ACCESS_KEY = os.getenv(
    "MINIO_ACCESS_KEY",
    "minioadmin",
)

MINIO_SECRET_KEY = os.getenv(
    "MINIO_SECRET_KEY",
    "minioadmin",
)

MINIO_SECURE = (
    os.getenv("MINIO_SECURE", "False").lower()
    == "true"
)

MINIO_BUCKET_NAME = os.getenv(
    "MINIO_BUCKET_NAME",
    "weather-data-lake",
)

MINIO_OBJECT_NAME = os.getenv(
    "MINIO_OBJECT_NAME",
    "weather_week5.parquet",
)

# Dash Configuration

W6_DASH_HOST = os.getenv(
    "W6_DASH_HOST",
    "0.0.0.0",
)

W6_DASH_PORT = int(
    os.getenv("W6_DASH_PORT", "8050")
)

W6_DASH_DEBUG = (
    os.getenv("W6_DASH_DEBUG", "True").lower()
    == "true"
)

# Week 5 Spark Dataset

WEEK5_CANDIDATES = [
    BASE_DIR / "w5_spark_weather_etl",
    BASE_DIR / "w5",
]

LOCAL_PARQUET_PATH = None

for week5_dir in WEEK5_CANDIDATES:

    candidate = (
        week5_dir
        / "data"
        / "processed"
        / "weather_week5.parquet"
    )

    if candidate.exists():
        LOCAL_PARQUET_PATH = candidate
        break

if LOCAL_PARQUET_PATH is None:

    LOCAL_PARQUET_PATH = (
        WEEK5_CANDIDATES[0]
        / "data"
        / "processed"
        / "weather_week5.parquet"
    )

# Local Download Directory

LOCAL_DATA_DIR = PROJECT_DIR / "data"

LOCAL_DOWNLOAD_PATH = (
    LOCAL_DATA_DIR
    / "weather_week5.parquet"
)
