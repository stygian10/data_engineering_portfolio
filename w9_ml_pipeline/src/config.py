from pathlib import Path

# Project Root

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Input Paths

FEATURE_DATA_PATH = (
    PROJECT_ROOT.parent
    / "w7_feature_engineering"
    / "data"
    / "processed"
    / "w7_features_final.parquet"
)

MODEL_PATH = (
    PROJECT_ROOT.parent
    / "w8_weather_prediction_model"
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

# Logging

LOG_DIR = PROJECT_ROOT / "logs"

# Create Required Directories

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)