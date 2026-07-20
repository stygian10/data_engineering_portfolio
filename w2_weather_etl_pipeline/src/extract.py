import pandas as pd

from config import INPUT_FILE


def extract():
    """
    Extract weather data from the W1 processed CSV file.
    """

    print(f"Reading data from: {INPUT_FILE}")

    df = pd.read_csv(
        INPUT_FILE,
        parse_dates=["time"]
    )

    print(f"Rows Loaded : {len(df):,}")
    print(f"Columns     : {len(df.columns)}")
    print(f"Cities      : {df['city'].nunique()}")
    print(f"Date Range  : {df['time'].min()} -> {df['time'].max()}")

    return df