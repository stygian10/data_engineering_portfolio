import os
from pathlib import Path

# Project Root

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# Data Directories

RAW_DATA_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
)

PROCESSED_DATA_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)


# Output Dataset

OUTPUT_DATA_PATH = (
    PROCESSED_DATA_DIR
    / "w7_features_final.parquet"
)


# MinIO Configuration

MINIO_ENDPOINT = os.getenv(
    "MINIO_ENDPOINT",
    "localhost:9000"
)

MINIO_ACCESS_KEY = os.getenv(
    "MINIO_ACCESS_KEY",
    "minioadmin"
)

MINIO_SECRET_KEY = os.getenv(
    "MINIO_SECRET_KEY",
    "minioadmin"
)

MINIO_BUCKET_NAME = os.getenv(
    "MINIO_BUCKET_NAME",
    "weather-data-lake"
)

# Week 6 uploads a single parquet object
MINIO_OBJECT_NAME = os.getenv(
    "MINIO_OBJECT_NAME",
    "weather_week5.parquet"
)


# Local Download Path

LOCAL_PARQUET_PATH = (
    RAW_DATA_DIR
    / "weather_week5.parquet"
)


# Create Required Directories

RAW_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

PROCESSED_DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)