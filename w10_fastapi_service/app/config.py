from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

# Docker Paths

DOCKER_MODEL_PATH = Path(
    "/workspace/w8_weather_prediction_model/models/linear_regression_model.pkl"
)

DOCKER_MODEL_METRICS_PATH = Path(
    "/workspace/w8_weather_prediction_model/models/model_metrics.json"
)

# Local Paths

PROJECT_ROOT = Path(__file__).resolve().parents[2]

LOCAL_MODEL_PATH = (
    PROJECT_ROOT
    / "w8_weather_prediction_model"
    / "models"
    / "linear_regression_model.pkl"
)

LOCAL_MODEL_METRICS_PATH = (
    PROJECT_ROOT
    / "w8_weather_prediction_model"
    / "models"
    / "model_metrics.json"
)

# Environment Detection
if DOCKER_MODEL_PATH.exists():

    MODEL_PATH = DOCKER_MODEL_PATH

    MODEL_METRICS_PATH = DOCKER_MODEL_METRICS_PATH

    logging.info("Running inside Docker")

else:

    MODEL_PATH = LOCAL_MODEL_PATH

    MODEL_METRICS_PATH = LOCAL_MODEL_METRICS_PATH

    logging.info("Running locally")

# Logging

logging.info(f"Model Path: {MODEL_PATH}")
logging.info(f"Model Metrics Path: {MODEL_METRICS_PATH}")