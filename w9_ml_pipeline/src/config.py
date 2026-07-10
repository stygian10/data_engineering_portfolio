from pathlib import Path

# Project Root

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Detect whether the project is running inside Airflow Docker

AIRFLOW_ROOT = Path("/opt/airflow")

if AIRFLOW_ROOT.exists():

    PORTFOLIO_ROOT = AIRFLOW_ROOT

    W7_FOLDER = "w7"
    W8_FOLDER = "w8"

else:

    PORTFOLIO_ROOT = PROJECT_ROOT.parent

    W7_FOLDER = "w7_feature_engineering"
    W8_FOLDER = "w8_weather_prediction_model"

# Input Paths

FEATURE_DATA_PATH = (
    PORTFOLIO_ROOT
    / W7_FOLDER
    / "data"
    / "processed"
    / "w7_features_final.parquet"
)

MODEL_PATH = (
    PORTFOLIO_ROOT
    / W8_FOLDER
    / "models"
    / "linear_regression_model.pkl"
)

# 
# Output Paths

OUTPUT_DIR = PROJECT_ROOT / "data" / "predictions"

PREDICTION_CSV = OUTPUT_DIR / "weather_predictions.csv"

PREDICTION_PARQUET = OUTPUT_DIR / "weather_predictions.parquet"

# Constants

PREDICTION_COLUMN = "predicted_temperature"

# MinIO Configuration

MINIO_ENDPOINT = "http://minio:9000"

MINIO_ACCESS_KEY = "minioadmin"

MINIO_SECRET_KEY = "minioadmin"

MINIO_BUCKET = "weather-data-lake"

MINIO_SECURE = False

MINIO_PREFIX = "predictions/"

# Logging

LOG_DIR = PROJECT_ROOT / "logs"

# Create Required Directories

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)