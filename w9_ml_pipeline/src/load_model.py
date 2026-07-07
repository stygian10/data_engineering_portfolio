import joblib

from config import MODEL_PATH


def load_model():
    """
    Load the trained machine learning model.

    Returns
    -------
    BaseEstimator
        Trained scikit-learn model.
    """

    # Check if model exists

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found:\n{MODEL_PATH}"
        )

    # Load model

    model = joblib.load(MODEL_PATH)

    # Confirmation

    print("Model loaded successfully.")
    print(f"Model path: {MODEL_PATH}")

    return model

#test
