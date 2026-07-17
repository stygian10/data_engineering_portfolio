from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

DOCKER_MODEL_PATH = Path(
    "/app/w8_weather_prediction_model/models/linear_regression_model.pkl"
)

LOCAL_MODEL_PATH = (
    Path(__file__).resolve().parents[2]
    / "w8_weather_prediction_model"
    / "models"
    / "linear_regression_model.pkl"
)

if DOCKER_MODEL_PATH.exists():
    MODEL_PATH = DOCKER_MODEL_PATH
    logging.info("Running inside Docker")
else:
    MODEL_PATH = LOCAL_MODEL_PATH
    logging.info("Running locally")

logging.info(f"Model Path: {MODEL_PATH}")