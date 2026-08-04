from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[2]

# Input Data

W2_DATA_FILE = os.getenv("W2_DATA_FILE")

if not W2_DATA_FILE:
    raise ValueError(
        "Environment variable 'W2_DATA_FILE' is not set."
    )

DATA_FILE = BASE_DIR / Path(W2_DATA_FILE)

# PostgreSQL Configuration

POSTGRES_HOST = os.getenv("POSTGRES_HOST")

POSTGRES_PORT = int(
    os.getenv("POSTGRES_PORT", "5432")
)

POSTGRES_DB = os.getenv("POSTGRES_DB")

POSTGRES_USER = os.getenv("POSTGRES_USER")

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Database Table

TABLE_NAME = "weather_data"