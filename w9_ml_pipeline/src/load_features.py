import pandas as pd

from config import FEATURE_DATA_PATH


def load_features():
    """
    Load the engineered feature dataset.

    Returns
    -------
    pandas.DataFrame
        Feature dataset.
    """

    # Check if the dataset exists
    if not FEATURE_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Feature dataset not found:\n{FEATURE_DATA_PATH}"
        )

    # Load the dataset
    features_df = pd.read_parquet(FEATURE_DATA_PATH)

    # Display dataset information
    print("Feature dataset loaded successfully.")
    print(f"Dataset path: {FEATURE_DATA_PATH}")
    print(f"Shape: {features_df.shape}")

    # Display column names
    print("\nColumns:")

    for column in features_df.columns:
        print(f"- {column}")

    # Display missing values
    print("\nMissing values:")

    print(features_df.isnull().sum())

    return features_df

