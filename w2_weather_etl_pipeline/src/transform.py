import pandas as pd


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform the extracted weather data into a PostgreSQL-ready format.
    """

    print("Transforming data...")

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    # Ensure datetime format
    df["time"] = pd.to_datetime(df["time"])

    # Standardize city names
    df["city"] = (
        df["city"]
        .str.strip()
        .str.title()
    )

    # Sort records
    df = (
        df.sort_values(["city", "time"])
          .reset_index(drop=True)
    )

    # Add data source
    df["source"] = "archive"

    print("Transformation complete.")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    return df