import os
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Week 6 project directory
PROJECT_DIR = Path(__file__).resolve().parents[1]

# MinIO Configuration
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_SECURE = False

# MinIO Bucket
BUCKET_NAME = "weather-data-lake"
OBJECT_PREFIX = "weather_week5.parquet"

# ------------------------------------------------------------------
# Week 5 Spark Dataset
# Works in both:
# - Local development (w5_spark_weather_etl)
# - Docker / Airflow (w5)
# ------------------------------------------------------------------

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

# ------------------------------------------------------------------
# Local Download Directory
# ------------------------------------------------------------------

LOCAL_DATA_DIR = PROJECT_DIR / "data"

LOCAL_DOWNLOAD_PATH = (
    LOCAL_DATA_DIR
    / "weather_week5.parquet"
)