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

# Week 5 Spark Dataset
LOCAL_PARQUET_PATH = (
    BASE_DIR
    / "w5_spark_weather_etl"
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