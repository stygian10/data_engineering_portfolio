from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_FILE = Path(
    os.getenv(
        "W2_DATA_FILE",
        str(
            BASE_DIR
            / "w2_weather_etl_pipeline"
            / "data"
            / "processed"
            / "weather_ready_for_postgres.csv"
        ),
    )
)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "airflow")
DB_USER = os.getenv("DB_USER", "airflow")
DB_PASSWORD = os.getenv("DB_PASSWORD", "airflow")

TABLE_NAME = "weather_data"