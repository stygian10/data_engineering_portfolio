import pandas as pd

from .config import (
    TARGET_COLUMN,
    TIME_COLUMN,
    PREDICTION_COLUMN,
)


def predict(model, scaler, features_df):
    """
    Generate weather predictions using the trained model.

    Parameters
    ----------
    model : BaseEstimator
        Trained Scikit-learn model.

    scaler : StandardScaler
        Trained scaler from Week 8.

    features_df : pandas.DataFrame
        Engineered feature dataset.

    Returns
    -------
    pandas.DataFrame
        Original dataset with predictions.
    """

    # Create a copy of the dataset
    prediction_df = features_df.copy()

    # Prepare feature matrix
    X = prediction_df.drop(
        columns=[
            TIME_COLUMN,
            TARGET_COLUMN,
        ]
    )

    # Convert features to float64
    X = X.astype("float64")

    # Apply scaler
    X_scaled = scaler.transform(X)

    # Preserve feature names after scaling
    X_scaled = pd.DataFrame(
        X_scaled,
        columns=X.columns,
        index=X.index,
    )

    # Generate predictions
    predictions = model.predict(X_scaled)

    # Add predictions to dataframe
    prediction_df[PREDICTION_COLUMN] = predictions

    # Display summary
    print("\nPredictions generated successfully.")
    print(f"Rows processed: {len(prediction_df)}")
    print(f"Prediction column: {PREDICTION_COLUMN}")

    return prediction_df