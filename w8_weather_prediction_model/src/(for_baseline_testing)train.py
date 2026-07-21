# W8 - BASELINE TRAINING SCRIPT
# Goal:
# Train a baseline Linear Regression model
# using the engineered Week 7 dataset.


# IMPORT LIBRARIES


import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

from config import (
    DATA_PATH,
    TARGET_COLUMN,
    RANDOM_STATE,
    TEST_SIZE,
    LINEAR_MODEL_PATH,
    SCALER_PATH
)


# LOAD DATASET


print("Loading dataset...")

df = pd.read_parquet(DATA_PATH)

print("Dataset loaded successfully.")

print("\nDataset Shape:")
print(df.shape)

print("\nFirst 5 Rows:")
print(df.head())


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

print("\nFeature Columns:")
print(X.columns)

print(f"\nTotal Features: {X.shape[1]}")


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


# SCALE FEATURES


print("\nScaling numerical features...")

scaler = StandardScaler()

numerical_columns = X_train.select_dtypes(
    include=["number"]
).columns

X_train = X_train.copy()
X_test = X_test.copy()

X_train[numerical_columns] = scaler.fit_transform(
    X_train[numerical_columns]
)

X_test[numerical_columns] = scaler.transform(
    X_test[numerical_columns]
)

joblib.dump(
    scaler,
    SCALER_PATH
)

print(f"Scaler saved to: {SCALER_PATH}")


# TRAIN BASELINE MODEL


print("\nTraining Linear Regression Model...")

model = LinearRegression()

model.fit(
    X_train,
    y_train
)

print("Model training completed.")


# SAVE MODEL


joblib.dump(
    model,
    LINEAR_MODEL_PATH
)

print(f"\nModel saved to: {LINEAR_MODEL_PATH}")

print("\nBaseline training completed successfully.")