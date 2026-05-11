#Goal: Build a reusable feature engineering pipeline that converts your W7D1 dataset into an ML-ready dataset.

import pandas as pd
import numpy as np  
from sklearn.preprocessing import StandardScaler
# ---------------------------
# STANDARDISE COLUMNS
# ---------------------------
def standardise_columns(df):
    column_mapping = {
        "avg_temp": "temperature",
        "max_temp": "temp_max",
        "min_temp": "temp_min",
        "avg_humidity": "humidity",
        "avg_windspeed": "windspeed",
    
    }

    df = df.rename(columns=column_mapping)
    return df
# ---------------------------
# TIME FEATURES
# ---------------------------
def create_time_features(df):
    df["date"] = pd.to_datetime(df["date"])

    df["day_of_week"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month
    df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)

    return df


# ---------------------------
# ROLLING FEATURES
# ---------------------------
def create_rolling_features(df, window=3):
    df = df.sort_values(by=["city", "date"])

    # Temperature rolling
    df["temp_rolling_mean"] = df.groupby("city")["temperature"].transform(
        lambda x: x.rolling(window).mean()
    )

    # Humidity rolling
    df["humidity_rolling_mean"] = df.groupby("city")["humidity"].transform(
        lambda x: x.rolling(window).mean()
    )

    # Wind rolling
    df["windspeed_rolling_mean"] = df.groupby("city")["windspeed"].transform(
        lambda x: x.rolling(window).mean()
    )

    return df

# ---------------------------
# LAG FEATURES
# ---------------------------
def create_lag_features(df):

    # Ensure correct time ordering
    df = df.sort_values(by=["city", "date"])

    # Temperature lag features
    df["temp_lag_1"] = (
        df.groupby("city")["temperature"].shift(1)
    )

    df["temp_lag_3"] = (
        df.groupby("city")["temperature"].shift(3)
    )

    # Humidity lag feature
    df["humidity_lag_1"] = (
        df.groupby("city")["humidity"].shift(1)
    )

    # Windspeed lag feature
    df["windspeed_lag_1"] = (
        df.groupby("city")["windspeed"].shift(1)
    )

    return df

# ---------------------------
# DELTA FEATURES
# ---------------------------
def create_delta_features(df):

    # Temperature change
    df["temp_delta"] = (
        df["temperature"] - df["temp_lag_1"]
    )

    # Humidity change
    df["humidity_delta"] = (
        df["humidity"] - df["humidity_lag_1"]
    )

    # Windspeed change
    df["windspeed_delta"] = (
        df["windspeed"] - df["windspeed_lag_1"]
    )

    return df

# ---------------------------
# PERCENTAGE CHANGE FEATURES
# ---------------------------
def create_pct_change_features(df):

    # Temperature percentage change
    df["temp_pct_change"] = (
        df.groupby("city")["temperature"].pct_change()
    )

    # Humidity percentage change
    df["humidity_pct_change"] = (
        df.groupby("city")["humidity"].pct_change()
    )

    # Windspeed percentage change
    df["windspeed_pct_change"] = (
        df.groupby("city")["windspeed"].pct_change()
    )

    return df

# ---------------------------
# TARGET VARIABLE
# ---------------------------
def create_target_variable(df):

    # Predict next day's temperature
    df["target_temp_next_day"] = (
        df.groupby("city")["temperature"].shift(-1)
    )

    return df

# ---------------------------
# SCALE FEATURES
# ---------------------------
def scale_features(df):

    scaler = StandardScaler()

    columns_to_scale = [

        # Core weather metrics
        "temperature",
        "humidity",
        "windspeed",

        # Rolling features
        "temp_rolling_mean",
        "humidity_rolling_mean",
        "windspeed_rolling_mean",

        # Lag features
        "temp_lag_1",
        "temp_lag_3",
        "humidity_lag_1",
        "windspeed_lag_1",

        # Delta features
        "temp_delta",
        "humidity_delta",
        "windspeed_delta",

        # Percentage change features
        "temp_pct_change",
        "humidity_pct_change",
        "windspeed_pct_change"

    ]

    df[columns_to_scale] = scaler.fit_transform(
        df[columns_to_scale]
    )

    return df

# ---------------------------
# VALIDATE DATASET
# ---------------------------
def validate_dataset(df):

    print("\n---------------------------")
    print("DATASET VALIDATION")
    print("---------------------------")

    # Final dataset shape
    print("\nFinal Shape:")
    print(df.shape)

    # Missing values
    print("\nMissing Values:")
    print(df.isnull().sum().sort_values(ascending=False))

    # Duplicate rows
    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    # Infinite values
    print("\nInfinite Values:")
    print(np.isinf(df.select_dtypes(include=[np.number])).sum())

    # Data types
    print("\nData Types:")
    print(df.dtypes)

    # Assertions
    assert df.duplicated().sum() == 0, "Duplicate rows detected"

    return df

# ---------------------------
# ENCODING FEATURES
# ---------------------------
def encode_categorical(df):
    if "city" in df.columns:
        df = pd.get_dummies(df, columns=["city"], drop_first=True)
    return df


# ---------------------------
# HANDLE MISSING VALUES
# ---------------------------
def handle_missing_values(df):
    df = df.bfill().ffill()
    return df


# ---------------------------
# MAIN FEATURE PIPELINE
# ---------------------------
def run_feature_pipeline(df):
    df = standardise_columns(df)
    df = create_time_features(df)
    df = create_rolling_features(df)
    df = create_lag_features(df)
    df = create_delta_features(df)
    df = create_pct_change_features(df)
    df = create_target_variable(df)
    df = handle_missing_values(df)
    df = scale_features(df)
    df = validate_dataset(df)
    df = encode_categorical(df)

    return df