# Loads the model once and caches it

import joblib

from app.config import MODEL_PATH

_model = None


def load_model():
    global _model

    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

        _model = joblib.load(MODEL_PATH)

    return _model