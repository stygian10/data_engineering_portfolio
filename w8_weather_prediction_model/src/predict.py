# W8 - WEATHER PREDICTION SCRIPT
# Purpose: Load the trained Random Forest model and predict tomorrow's temperature using the latest engineered dataset.

import joblib
import pandas as pd

from config import (
    DATA_PATH,
    TARGET_COLUMN
)

# Load Trained Model

print("Loading trained model...")

model = joblib.load(
    "models/random_forest_model.pkl"
)

print("Model loaded successfully.")

# Load Latest Feature Dataset

print("\nLoading feature dataset...")

df = pd.read_parquet(DATA_PATH)

print("Dataset loaded successfully.")

print("\nDataset Shape:")
print(df.shape)

print("\nLatest Date:")
print(df["date"].max())

# Remove Missing Values

df = df.dropna()

# Select Latest Record

latest_record = df.iloc[[-1]]

print("\nUsing Latest Record")
print(latest_record[["date"]])

# -----------------------------------
# Prepare Features
# -----------------------------------

X = latest_record.drop(
    columns=[
        TARGET_COLUMN,
        "date"
    ]
)

# -----------------------------------
# Actual Target
# -----------------------------------

actual_temperature = latest_record[
    TARGET_COLUMN
].values[0]

# -----------------------------------
# Make Prediction
# -----------------------------------

prediction = model.predict(X)

predicted_temperature = prediction[0]

# -----------------------------------
# Display Results
# -----------------------------------

print("\nPrediction Results")
print("-" * 40)

print(
    f"Actual Temperature     : {actual_temperature:.2f} °C"
)

print(
    f"Predicted Temperature  : {predicted_temperature:.2f} °C"
)

print(
    f"Prediction Error       : "
    f"{abs(actual_temperature - predicted_temperature):.2f} °C"
)

print("\nPrediction completed successfully.")