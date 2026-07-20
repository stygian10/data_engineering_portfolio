import pandas as pd


def validate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate the transformed weather data.
    """

    print("Validating data...")

    required_columns = [
        "time",
        "temperature_2m",
        "relative_humidity_2m",
        "wind_speed_10m",
        "city",
        "source"
    ]

    # Check required columns
    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Check datetime type
    if not pd.api.types.is_datetime64_any_dtype(df["time"]):
        raise TypeError("'time' column must be datetime.")

    # Check for missing values
    if df[required_columns].isnull().any().any():
        raise ValueError("Dataset contains missing values.")

    # Check duplicate city/time records
    duplicate_rows = df.duplicated(
        subset=["city", "time"],
        keep=False
    )

    if duplicate_rows.any():
        raise ValueError(
            f"Duplicate city/time records found: {duplicate_rows.sum()}"
        )

    # Temperature range
    if not df["temperature_2m"].between(-60, 60).all():
        raise ValueError("Temperature values are outside the valid range.")

    # Humidity range
    if not df["relative_humidity_2m"].between(0, 100).all():
        raise ValueError("Humidity values are outside the valid range.")

    # Wind speed range
    if (df["wind_speed_10m"] < 0).any():
        raise ValueError("Negative wind speed values found.")

    print("Validation successful.")
    print(f"Rows Validated: {len(df):,}")

    return df