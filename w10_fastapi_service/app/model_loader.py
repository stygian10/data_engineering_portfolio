import logging

import joblib

from app.config import MODEL_PATH, SCALER_PATH

logging.basicConfig(level=logging.INFO)

logging.info(f"Model Path: {MODEL_PATH}")
logging.info(f"Scaler Path: {SCALER_PATH}")

# Cache loaded objects

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

    # Return cached objects if already loaded

    if _model is not None and _scaler is not None:
        return _model, _scaler

    # Validate model

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found:\n{MODEL_PATH}"
        )

    # Validate scaler

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