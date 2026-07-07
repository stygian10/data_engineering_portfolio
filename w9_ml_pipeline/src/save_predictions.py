import pandas as pd

from config import (
    OUTPUT_DIR,
    PREDICTION_CSV,
    PREDICTION_PARQUET
)


def save_predictions(prediction_df):
    """
    Save prediction results as CSV and Parquet.

    Parameters
    ----------
    prediction_df : pandas.DataFrame
        Prediction results.

    Returns
    -------
    tuple
        CSV and Parquet file paths.
    """

    # Ensure output directory exists
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save CSV
    prediction_df.to_csv(
        PREDICTION_CSV,
        index=False
    )

    # Save Parquet
    prediction_df.to_parquet(
        PREDICTION_PARQUET,
        index=False
    )

    # Display summary
    print("Predictions saved successfully.")
    print(f"CSV Output: {PREDICTION_CSV}")
    print(f"Parquet Output: {PREDICTION_PARQUET}")

    return (
        PREDICTION_CSV,
        PREDICTION_PARQUET
    )