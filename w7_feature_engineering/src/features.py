import numpy as np
import pandas as pd


# STANDARDISE COLUMNS


def standardise_columns(df):

    column_mapping = {
        "temperature_2m": "temperature",
        "relative_humidity_2m": "humidity",
        "wind_speed_10m": "windspeed",
    }

    df = df.rename(columns=column_mapping)

    return df


# CLEAN DATASET


def clean_dataset(df):

    df = df.copy()

    df = df.sort_values(
        by=["city", "time"]
    )

    df = df.drop_duplicates()

    df = df.drop(
        columns=["id", "created_at", "date"],
        errors="ignore"
    )

    return df


# TIME FEATURES


def create_time_features(df):

    df["time"] = pd.to_datetime(df["time"])

    df["year"] = df["time"].dt.year

    df["month"] = df["time"].dt.month

    df["day"] = df["time"].dt.day

    df["hour"] = df["time"].dt.hour

    df["day_of_week"] = df["time"].dt.dayofweek

    df["week_of_year"] = (
        df["time"]
        .dt.isocalendar()
        .week
        .astype(int)
    )

    df["day_of_year"] = (
        df["time"]
        .dt.dayofyear
    )

    df["is_weekend"] = (
        df["day_of_week"] >= 5
    ).astype(int)

    return df


# ROLLING FEATURES


def create_rolling_features(df):

    df["temp_rolling_mean"] = (
        df.groupby("city")["temperature"]
        .transform(
            lambda x: x.rolling(
                window=3,
                min_periods=1
            ).mean()
        )
    )

    df["humidity_rolling_mean"] = (
        df.groupby("city")["humidity"]
        .transform(
            lambda x: x.rolling(
                window=3,
                min_periods=1
            ).mean()
        )
    )

    df["windspeed_rolling_mean"] = (
        df.groupby("city")["windspeed"]
        .transform(
            lambda x: x.rolling(
                window=3,
                min_periods=1
            ).mean()
        )
    )

    return df


# LAG FEATURES


def create_lag_features(df):

    df["temp_lag_1"] = (
        df.groupby("city")["temperature"]
        .shift(1)
    )

    df["temp_lag_3"] = (
        df.groupby("city")["temperature"]
        .shift(3)
    )

    df["humidity_lag_1"] = (
        df.groupby("city")["humidity"]
        .shift(1)
    )

    df["windspeed_lag_1"] = (
        df.groupby("city")["windspeed"]
        .shift(1)
    )

    return df


# DELTA FEATURES


def create_delta_features(df):

    df["temp_delta"] = (
        df["temperature"]
        - df["temp_lag_1"]
    )

    df["humidity_delta"] = (
        df["humidity"]
        - df["humidity_lag_1"]
    )

    df["windspeed_delta"] = (
        df["windspeed"]
        - df["windspeed_lag_1"]
    )

    return df


# PERCENTAGE CHANGE FEATURES


def create_pct_change_features(df):

    df["temp_pct_change"] = (
        df.groupby("city")["temperature"]
        .pct_change()
        .replace([np.inf, -np.inf], 0)
        .fillna(0)
    )

    df["humidity_pct_change"] = (
        df.groupby("city")["humidity"]
        .pct_change()
        .replace([np.inf, -np.inf], 0)
        .fillna(0)
    )

    df["windspeed_pct_change"] = (
        df.groupby("city")["windspeed"]
        .pct_change()
        .replace([np.inf, -np.inf], 0)
        .fillna(0)
    )

    return df


# TARGET VARIABLE


def create_target_variable(df):

    df["target_temp_next_hour"] = (
        df.groupby("city")["temperature"]
        .shift(-1)
    )

    return df
# HANDLE MISSING VALUES


def handle_missing_values(df):

    df = df.replace([np.inf, -np.inf], np.nan)

    df = (
        df
        .bfill()
        .ffill()
    )

    return df


# ENCODE CATEGORICAL


def encode_categorical(df):

    if "city" in df.columns:

        df = pd.get_dummies(
            df,
            columns=["city"],
            drop_first=True
        )

    if "source" in df.columns:

        df = pd.get_dummies(
            df,
            columns=["source"],
            drop_first=True
        )

    bool_columns = df.select_dtypes(
        include="bool"
    ).columns

    df[bool_columns] = (
        df[bool_columns]
        .astype(int)
    )

    return df


# VALIDATE DATASET


def validate_dataset(df):

    print("\n---------------------------")
    print("DATASET VALIDATION")
    print("---------------------------")

    print("\nFinal Shape:")
    print(df.shape)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\nInfinite Values:")
    print(
        np.isinf(
            df.select_dtypes(include=[np.number])
        ).sum()
    )

    print("\nData Types:")
    print(df.dtypes)

    assert (
        df.duplicated().sum() == 0
    ), "Duplicate rows detected"

    assert (
        np.isinf(
            df.select_dtypes(include=[np.number])
        ).sum().sum() == 0
    ), "Infinite values detected"

    return df


# MAIN FEATURE PIPELINE


def run_feature_pipeline(df):

    print("\nStandardising columns...")
    df = standardise_columns(df)

    print("Cleaning dataset...")
    df = clean_dataset(df)

    print("Creating time features...")
    df = create_time_features(df)

    print("Creating rolling features...")
    df = create_rolling_features(df)

    print("Creating lag features...")
    df = create_lag_features(df)

    print("Creating delta features...")
    df = create_delta_features(df)

    print("Creating percentage change features...")
    df = create_pct_change_features(df)

    print("Creating target variable...")
    df = create_target_variable(df)

    print("Handling missing values...")
    df = handle_missing_values(df)

    print("Encoding categorical features...")
    df = encode_categorical(df)

    print("Validating dataset...")
    df = validate_dataset(df)

    return df