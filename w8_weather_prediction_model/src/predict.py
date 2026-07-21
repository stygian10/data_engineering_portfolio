# W8 - WEATHER PREDICTION SCRIPT
# Purpose:
# Load the trained model and scaler, then predict the
# next hour temperature using the latest engineered dataset.


# IMPORT LIBRARIES


import joblib
import pandas as pd

from config import (
    DATA_PATH,
    TARGET_COLUMN,
    BEST_MODEL_PATH,
    SCALER_PATH
)


# LOAD TRAINED MODEL


print("Loading trained model...")

model = joblib.load(
    BEST_MODEL_PATH
)

print("Model loaded successfully.")


# LOAD SCALER


print("\nLoading scaler...")

scaler = joblib.load(
    SCALER_PATH
)

print("Scaler loaded successfully.")


# LOAD FEATURE DATASET


print("\nLoading feature dataset...")

df = pd.read_parquet(DATA_PATH)

print("Dataset loaded successfully.")

print("\nDataset Shape:")
print(df.shape)

print("\nLatest Timestamp:")
print(df["time"].max())


# REMOVE MISSING VALUES


df = df.dropna()


# SELECT LATEST RECORD


latest_record = df.iloc[[-1]]

print("\nUsing Latest Record")

print(
    latest_record[["time"]]
)


# PREPARE FEATURES


X = latest_record.drop(
    columns=[
        TARGET_COLUMN,
        "time"
    ]
)


# ACTUAL TARGET


actual_temperature = latest_record[
    TARGET_COLUMN
].values[0]


# SCALE FEATURES


numerical_columns = X.select_dtypes(
    include=["number"]
).columns

X = X.copy()

X[numerical_columns] = scaler.transform(
    X[numerical_columns]
)


# MAKE PREDICTION


prediction = model.predict(X)

predicted_temperature = prediction[0]


# DISPLAY RESULTS


print("\nPrediction Results")

print("-" * 40)

print(
    f"Actual Temperature    : "
    f"{actual_temperature:.2f} °C"
)

print(
    f"Predicted Temperature : "
    f"{predicted_temperature:.2f} °C"
)

print(
    f"Prediction Error      : "
    f"{abs(actual_temperature - predicted_temperature):.2f} °C"
)

print("\nPrediction completed successfully.")