import logging

import pandas as pd

from app.model_loader import load_model

logging.basicConfig(level=logging.INFO)


def predict(features):
    """
    Generate a temperature prediction using the
    trained weather prediction model.

    Parameters
    ----------
    features : dict
        Dictionary containing the engineered
        feature values.

    Returns
    -------
    float
        Predicted next-hour temperature.
    """

    # Load trained model and scaler

    model, scaler = load_model()

    # Convert dictionary to DataFrame

    df = pd.DataFrame([features])

    # Expected feature order from training

    expected_features = list(
        model.feature_names_in_
    )

    # Validate missing features

    missing_features = [
        feature
        for feature in expected_features
        if feature not in df.columns
    ]

    if missing_features:

        raise ValueError(
            "Missing required features: "
            + ", ".join(missing_features)
        )

    # Remove unexpected features

    extra_features = [
        feature
        for feature in df.columns
        if feature not in expected_features
    ]

    if extra_features:

        logging.warning(
            "Ignoring unexpected features: %s",
            ", ".join(extra_features),
        )

        df = df.drop(
            columns=extra_features
        )

    # Match training feature order

    df = df.reindex(
        columns=expected_features
    )

    # Convert all values to numeric

    df = df.astype("float64")

    # Validate missing values

    if df.isnull().values.any():

        raise ValueError(
            "Prediction input contains "
            "missing values."
        )

    # Apply the same scaling used during training

    numerical_columns = df.select_dtypes(
        include=["number"]
    ).columns

    df = df.copy()

    df[numerical_columns] = scaler.transform(
        df[numerical_columns]
    )

    logging.info(
        "Generating prediction..."
    )

    prediction = model.predict(df)

    predicted_temperature = float(
        prediction[0]
    )

    logging.info(
        f"Prediction completed: "
        f"{predicted_temperature:.2f} °C"
    )

    return predicted_temperature