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
    print(f"Rows: {len(features_df)}")
    print(f"Columns: {len(features_df.columns)}")

    return features_df