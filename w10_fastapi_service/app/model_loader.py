from pathlib import Path
import logging

import joblib

logging.basicConfig(level=logging.INFO)

# --------------------------------------------------------
# Model paths
# --------------------------------------------------------

DOCKER_MODEL_PATH = Path(
    "/app/w8_weather_prediction_model/models/linear_regression_model.pkl"
)

LOCAL_MODEL_PATH = (
    Path(__file__).resolve().parents[2]
    / "w8_weather_prediction_model"
    / "models"
    / "linear_regression_model.pkl"
)

DOCKER_SCALER_PATH = Path(
    "/app/w8_weather_prediction_model/models/scaler.pkl"
)

LOCAL_SCALER_PATH = (
    Path(__file__).resolve().parents[2]
    / "w8_weather_prediction_model"
    / "models"
    / "scaler.pkl"
)

# --------------------------------------------------------
# Detect execution environment
# --------------------------------------------------------

if DOCKER_MODEL_PATH.is_file():

    MODEL_PATH = DOCKER_MODEL_PATH
    SCALER_PATH = DOCKER_SCALER_PATH

    logging.info("Running inside Docker")

else:

    MODEL_PATH = LOCAL_MODEL_PATH
    SCALER_PATH = LOCAL_SCALER_PATH

    logging.info("Running locally")

logging.info(f"Model Path: {MODEL_PATH}")
logging.info(f"Scaler Path: {SCALER_PATH}")

# --------------------------------------------------------
# Cache loaded objects
# --------------------------------------------------------

_model = None
_scaler = None


def load_model():
    """
    Load the trained model and scaler.

    Returns
    -------
    tuple
        (model, scaler)
    """

    global _model
    global _scaler

    if _model is not None and _scaler is not None:
        return _model, _scaler

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found:\n{MODEL_PATH}"
        )

    if not SCALER_PATH.exists():
        raise FileNotFoundError(
            f"Scaler file not found:\n{SCALER_PATH}"
        )

    logging.info("Loading trained model...")

    _model = joblib.load(MODEL_PATH)

    logging.info("Loading scaler...")

    _scaler = joblib.load(SCALER_PATH)

    logging.info(
        f"Loaded {_model.__class__.__name__} and "
        f"{_scaler.__class__.__name__}"
    )

    return _model, _scaler