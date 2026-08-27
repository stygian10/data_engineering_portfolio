import pandas as pd

from src.config import PROCESSED_DIR, OUTPUT_FILE


def load(df: pd.DataFrame) -> None:
    """
    Save the validated weather data for PostgreSQL loading.
    """

    print("Saving processed data...")

    # Create output directory if it doesn't exist
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Save CSV
    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Data saved successfully.")
    print(f"Output File : {OUTPUT_FILE}")
    print(f"Rows Saved  : {len(df):,}")