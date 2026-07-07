import pandas as pd

from config import PREDICTION_COLUMN


def predict(model, features_df):
    """
    Generate weather predictions using the trained model.

    Parameters
    ----------
    model : BaseEstimator
        Trained machine learning model.

    features_df : pandas.DataFrame
        Engineered feature dataset.

    Returns
    -------
    pandas.DataFrame
        Original dataset with predictions.
    """

    # Create a copy of the dataset
    prediction_df = features_df.copy()

    # Prepare the feature matrix
    X = prediction_df.drop(
        columns=[
            "date",
            "target_temp_next_day"
        ]
    )

    # Generate predictions
    predictions = model.predict(X)

    # Add predictions to the DataFrame
    prediction_df[PREDICTION_COLUMN] = predictions

    # Display summary
    print("Predictions generated successfully.")
    print(f"Rows processed: {len(prediction_df)}")
    print(f"Prediction column: {PREDICTION_COLUMN}")

    return prediction_df

    