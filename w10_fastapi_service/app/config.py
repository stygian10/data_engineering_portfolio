# Stores paths and configuration
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = (
    BASE_DIR
    / "w8_weather_prediction_model"
    / "models"
    / "linear_regression_model.pkl"
)

