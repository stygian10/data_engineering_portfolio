from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR.parent
    / "w1_weather_data_cleaner"
    / "data"
    / "processed"
    / "uk_weather_clean.csv"
)

RAW_DIR = BASE_DIR / "data" / "raw"

PROCESSED_DIR = BASE_DIR / "data" / "processed"

OUTPUT_FILE = PROCESSED_DIR / "weather_ready_for_postgres.csv"