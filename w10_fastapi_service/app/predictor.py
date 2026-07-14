# Contains prediction logic

import pandas as pd

from app.model_loader import load_model


def predict(features):

    model = load_model()

    df = pd.DataFrame([features])

    # Ensures feature order matches training
    df = df.reindex(columns=model.feature_names_in_)

    prediction = model.predict(df)

    return float(prediction[0])