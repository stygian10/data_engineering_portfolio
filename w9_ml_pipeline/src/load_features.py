import pandas as pd

from config import (
    FEATURE_DATA_PATH,
    TARGET_COLUMN,
    TIME_COLUMN
)


def load_features():
    """
    Load the engineered feature dataset.

    Returns
    -------
    pandas.DataFrame
        Engineered feature dataset.
    """

    # Check if the dataset exists
    if not FEATURE_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Feature dataset not found:\n{FEATURE_DATA_PATH}"
        )

    # Load the dataset
    features_df = pd.read_parquet(FEATURE_DATA_PATH)

    # Check if dataset is empty
    if features_df.empty:
        raise ValueError(
            "The feature dataset is empty."
        )

    # Validate required columns
    required_columns = [
        TIME_COLUMN,
        TARGET_COLUMN
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in features_df.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    # Display dataset information
    print("Feature dataset loaded successfully.")
    print(f"Dataset path: {FEATURE_DATA_PATH}")
    print(f"Rows: {len(features_df)}")
    print(f"Columns: {len(features_df.columns)}")

    print("\nDataset Time Range")
    print(
        f"Start: {features_df[TIME_COLUMN].min()}"
    )
    print(
        f"End  : {features_df[TIME_COLUMN].max()}"
    )

    print(
        f"\nTarget Column: {TARGET_COLUMN}"
    )

    return features_df