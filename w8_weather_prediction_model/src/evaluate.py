# W8 - MODEL EVALUATION SCRIPT
# Goal:
# Generate evaluation visualizations for the
# selected model using the test dataset.
#
# This script:
# - Loads the saved best model and scaler
# - Recreates the test dataset
# - Generates prediction visualizations
# - Saves evaluation figures


# IMPORT LIBRARIES


import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split

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
# Read the processed Week 7 feature dataset.


print("Loading dataset...")

df = pd.read_parquet(DATA_PATH)

print("Dataset loaded successfully.")

print("\nDataset Shape:")
print(df.shape)


# REMOVE MISSING VALUES
# Remove incomplete records before evaluation.


df = df.dropna()

print("\nDataset Shape After Dropping Nulls:")
print(df.shape)


# PREPARE FEATURES & TARGET
# Separate the input features from the target.


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
# Recreate the same train/test split used
# during model training.


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
# Load the saved scaler used during training.


print("\nLoading scaler...")

scaler = joblib.load(
    SCALER_PATH
)

print("Scaler loaded successfully.")


# SCALE FEATURES
# Apply the saved scaler to numerical features.


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


# LOAD BEST MODEL
# Load the selected model for evaluation.


print("\nLoading best model...")

model = joblib.load(
    BEST_MODEL_PATH
)

print("Best model loaded successfully.")


# MAKE PREDICTIONS
# Generate predictions using the saved model.


predictions = model.predict(
    X_test
)

# ACTUAL VS PREDICTED PLOT
# Compare the predicted values against
# the actual target values.


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

print(
    f"\nSaved: "
    f"{ACTUAL_VS_PREDICTED_FIGURE}"
)


# RESIDUAL DISTRIBUTION
# Visualize the prediction errors to
# assess model performance.


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

print(
    f"Saved: "
    f"{RESIDUAL_DISTRIBUTION_FIGURE}"
)


# SUMMARY
# Confirm that the evaluation figures
# were generated successfully.


print("\n" + "=" * 60)
print("EVALUATION VISUALIZATIONS COMPLETED")
print("=" * 60)

print(f"Best Model               : {BEST_MODEL_PATH}")
print(f"Actual vs Predicted Plot : {ACTUAL_VS_PREDICTED_FIGURE}")
print(f"Residual Distribution    : {RESIDUAL_DISTRIBUTION_FIGURE}")

print("\nWeek 8 evaluation completed successfully.")
