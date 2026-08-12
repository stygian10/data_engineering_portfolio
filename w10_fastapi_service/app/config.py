import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO)

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = Path(
    os.getenv(
        "MODEL_PATH",
        PROJECT_ROOT
        / "w8_weather_prediction_model"
        / "models"
        / "linear_regression_model.pkl",
    )
)

MODEL_METRICS_PATH = Path(
    os.getenv(
        "MODEL_METRICS_PATH",
        PROJECT_ROOT
        / "w8_weather_prediction_model"
        / "models"
        / "model_metrics.json",
    )
)

SCALER_PATH = Path(
    os.getenv(
        "SCALER_PATH",
        PROJECT_ROOT
        / "w8_weather_prediction_model"
        / "models"
        / "scaler.pkl",
    )
)

FEATURE_FILE = Path(
    os.getenv(
        "FEATURE_FILE",
        PROJECT_ROOT
        / "w7_feature_engineering"
        / "data"
        / "processed"
        / "w7_features_final.parquet",
    )
)

PREDICTION_FILE = Path(
    os.getenv(
        "PREDICTION_FILE",
        PROJECT_ROOT
        / "w9_ml_pipeline"
        / "data"
        / "predictions"
        / "weather_predictions.csv",
    )
)

logging.info(f"Model Path: {MODEL_PATH}")
logging.info(f"Scaler Path: {SCALER_PATH}")
logging.info(f"Model Metrics Path: {MODEL_METRICS_PATH}")
logging.info(f"Feature File: {FEATURE_FILE}")
logging.info(f"Prediction File: {PREDICTION_FILE}")