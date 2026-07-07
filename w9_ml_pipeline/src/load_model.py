import joblib

from config import MODEL_PATH


def load_model():
    """
    Load the trained machine learning model.

    Returns
    -------
    BaseEstimator
        Trained Scikit-learn model.
    """

    # Check if the model exists
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found:\n{MODEL_PATH}"
        )

    # Load the model
    model = joblib.load(MODEL_PATH)

    # Confirmation message
    print("\nModel loaded successfully.")
    print(f"Model path: {MODEL_PATH}")

    return model
