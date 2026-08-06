from pathlib import Path
import os

# =====================================================
# PostgreSQL
# =====================================================

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")

POSTGRES_PORT = int(
    os.getenv("POSTGRES_PORT", 5432)
)

POSTGRES_DB = os.getenv(
    "POSTGRES_DB",
    "airflow",
)

POSTGRES_USER = os.getenv(
    "POSTGRES_USER",
    "airflow",
)

POSTGRES_PASSWORD = os.getenv(
    "POSTGRES_PASSWORD",
    "airflow",
)

TABLE_NAME = os.getenv(
    "DB_TABLE_NAME",
    "weather_data",
)

# =====================================================
# Recovery Paths
# =====================================================

AIRFLOW_ROOT = Path("/opt/airflow")

W1_DIR = AIRFLOW_ROOT / "w1"
W2_DIR = AIRFLOW_ROOT / "w2"
W3_DIR = AIRFLOW_ROOT / "w3"

HISTORICAL_DATASET = (
    W2_DIR
    / "data"
    / "processed"
)