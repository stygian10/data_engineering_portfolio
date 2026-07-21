import joblib

from config import (
    BEST_MODEL_PATH,
    SCALER_PATH
)


def load_model():
    """
    Load the trained machine learning model and scaler.

    Returns
    -------
    tuple
        (trained_model, fitted_scaler)
    """

    # Check if the model exists
    if not BEST_MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found:\n{BEST_MODEL_PATH}"
        )

    # Check if the scaler exists
    if not SCALER_PATH.exists():
        raise FileNotFoundError(
            f"Scaler file not found:\n{SCALER_PATH}"
        )

    # Load the model
    model = joblib.load(BEST_MODEL_PATH)

    # Load the scaler
    scaler = joblib.load(SCALER_PATH)

    # Confirmation message
    print("\nModel loaded successfully.")
    print(f"Model path: {BEST_MODEL_PATH}")

    print("\nScaler loaded successfully.")
    print(f"Scaler path: {SCALER_PATH}")

    return model, scaler