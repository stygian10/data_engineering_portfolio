import matplotlib.pyplot as plt

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from .config import (
    TARGET_COLUMN,
    TIME_COLUMN,
    PREDICTION_COLUMN,
    PREDICTION_VS_ACTUAL_FIGURE,
    RESIDUAL_PLOT_FIGURE,
    ERROR_DISTRIBUTION_FIGURE,
)


def evaluate_predictions(prediction_df):
    """
    Evaluate prediction quality.

    Parameters
    ----------
    prediction_df : pandas.DataFrame
        Prediction dataset containing
        actual and predicted temperatures.
    """

    print("\nEvaluating prediction outputs...")

    # Actual vs Predicted

    y_true = prediction_df[TARGET_COLUMN]

    y_pred = prediction_df[PREDICTION_COLUMN]

    # Metrics

    mae = mean_absolute_error(
        y_true,
        y_pred
    )

    mse = mean_squared_error(
        y_true,
        y_pred
    )

    rmse = mse ** 0.5

    r2 = r2_score(
        y_true,
        y_pred
    )

    print("\nPrediction Metrics")

    print(f"MAE  : {mae:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"R²   : {r2:.2f}")

    # Prediction Error

    prediction_df["prediction_error"] = (
        y_true
        - y_pred
    )

    print("\nPrediction Error Summary")

    print(
        prediction_df[
            "prediction_error"
        ].describe()
    )

    # Sample Predictions

    print("\nSample Predictions")

    print(
        prediction_df[
            [
                TIME_COLUMN,
                TARGET_COLUMN,
                PREDICTION_COLUMN,
                "prediction_error",
            ]
        ].head(10)
    )

    # Prediction vs Actual

    plt.figure(figsize=(7, 7))

    plt.scatter(
        y_true,
        y_pred,
        alpha=0.7,
    )

    plt.xlabel("Actual Temperature")

    plt.ylabel("Predicted Temperature")

    plt.title("Prediction vs Actual")

    plt.tight_layout()

    plt.savefig(
        PREDICTION_VS_ACTUAL_FIGURE
    )

    plt.close()

    # Residual Plot

    plt.figure(figsize=(8, 5))

    plt.scatter(
        y_pred,
        prediction_df["prediction_error"],
        alpha=0.7,
    )

    plt.axhline(
        0,
        linestyle="--",
    )

    plt.xlabel("Predicted Temperature")

    plt.ylabel("Residual")

    plt.title("Residual Plot")

    plt.tight_layout()

    plt.savefig(
        RESIDUAL_PLOT_FIGURE
    )

    plt.close()

    # Error Distribution

    plt.figure(figsize=(8, 5))

    plt.hist(
        prediction_df["prediction_error"],
        bins=15,
    )

    plt.xlabel("Prediction Error")

    plt.ylabel("Frequency")

    plt.title("Prediction Error Distribution")

    plt.tight_layout()

    plt.savefig(
        ERROR_DISTRIBUTION_FIGURE
    )

    plt.close()

    print("\nSaved Figures")

    print(PREDICTION_VS_ACTUAL_FIGURE)

    print(RESIDUAL_PLOT_FIGURE)

    print(ERROR_DISTRIBUTION_FIGURE)

    return {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2,
    }