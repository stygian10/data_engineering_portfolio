# W8 - MODEL EVALUATION SCRIPT
# Goal:
# Evaluate the trained regression model using
# MAE, RMSE and R² metrics while generating
# prediction and residual visualization plots.


# IMPORT LIBRARIES


import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from config import (
    DATA_PATH,
    TARGET_COLUMN,
    RANDOM_STATE,
    TEST_SIZE,
    BEST_MODEL_PATH,
    SCALER_PATH,
    ACTUAL_VS_PREDICTED_FIGURE,
    RESIDUAL_DISTRIBUTION_FIGURE
)


# LOAD DATASET


print("Loading dataset...")

df = pd.read_parquet(DATA_PATH)

print("Dataset loaded successfully.")

print("\nDataset Shape:")
print(df.shape)


# REMOVE MISSING VALUES


df = df.dropna()

print("\nDataset Shape After Dropping Nulls:")
print(df.shape)


# PREPARE FEATURES & TARGET


X = df.drop(
    columns=[
        TARGET_COLUMN,
        "time"
    ]
)

y = df[TARGET_COLUMN]

print("\nFeature Shape:")
print(X.shape)

print("Target Shape:")
print(y.shape)


# TRAIN / TEST SPLIT


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE
)

print("\nTrain/Test Split Complete")

print(f"X_train Shape: {X_train.shape}")
print(f"X_test Shape : {X_test.shape}")


# LOAD SCALER


print("\nLoading scaler...")

scaler = joblib.load(
    SCALER_PATH
)

print("Scaler loaded successfully.")


# SCALE FEATURES


numerical_columns = X_train.select_dtypes(
    include=["number"]
).columns

X_train = X_train.copy()
X_test = X_test.copy()

X_train[numerical_columns] = scaler.transform(
    X_train[numerical_columns]
)

X_test[numerical_columns] = scaler.transform(
    X_test[numerical_columns]
)


# LOAD TRAINED MODEL


print("\nLoading trained model...")

model = joblib.load(
    BEST_MODEL_PATH
)

print("Model loaded successfully.")


# MAKE PREDICTIONS


predictions = model.predict(
    X_test
)


# EVALUATION METRICS


mae = mean_absolute_error(
    y_test,
    predictions
)

mse = mean_squared_error(
    y_test,
    predictions
)

rmse = mse ** 0.5

r2 = r2_score(
    y_test,
    predictions)


print("\nMODEL PERFORMANCE")
print("-" * 40)

print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.2f}")


# ACTUAL VS PREDICTED PLOT


plt.figure(figsize=(8, 6))

plt.scatter(
    y_test,
    predictions
)

plt.xlabel("Actual Values")

plt.ylabel("Predicted Values")

plt.title("Actual vs Predicted")

plt.tight_layout()

plt.savefig(
    ACTUAL_VS_PREDICTED_FIGURE,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(f"\nSaved: {ACTUAL_VS_PREDICTED_FIGURE}")


# RESIDUAL DISTRIBUTION


residuals = (
    y_test -
    predictions
)

plt.figure(figsize=(8, 6))

plt.hist(
    residuals,
    bins=30
)

plt.xlabel("Residual Error")

plt.ylabel("Frequency")

plt.title("Residual Distribution")

plt.tight_layout()

plt.savefig(
    RESIDUAL_DISTRIBUTION_FIGURE,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(f"Saved: {RESIDUAL_DISTRIBUTION_FIGURE}")


print("\nEvaluation completed successfully.")