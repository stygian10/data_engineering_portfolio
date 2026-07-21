from load_model import load_model
from load_features import load_features
from predict import predict
from save_predictions import save_predictions
from evaluate_predictions import evaluate_predictions

# from upload_to_minio import upload_predictions
"""Uploading is handled separately by the Airflow pipeline."""


def main():
    """
    Execute the complete machine learning inference pipeline,
    including model loading, feature loading, prediction,
    evaluation, and prediction file creation.
    """

    # Load the trained model and scaler
    print("Loading trained model and scaler...")

    model, scaler = load_model()

    # Load the feature dataset
    print("\nLoading feature dataset...")

    features_df = load_features()

    # Generate predictions
    print("\nGenerating predictions...")

    prediction_df = predict(
        model,
        scaler,
        features_df
    )

    # Evaluate predictions
    print("\nEvaluating predictions...")

    metrics = evaluate_predictions(
        prediction_df
    )

    # Save prediction files
    print("\nSaving prediction files...")

    save_predictions(
        prediction_df
    )

    # Upload prediction files to MinIO
    # print("\nUploading prediction files to MinIO...")
    # upload_predictions()

    # Display summary
    print("\nPrediction Summary")
    print("-" * 40)

    print(f"Prediction Records : {len(prediction_df)}")
    print(f"MAE                : {metrics['MAE']:.2f}")
    print(f"RMSE               : {metrics['RMSE']:.2f}")
    print(f"R²                 : {metrics['R2']:.2f}")

    # Display sample predictions
    print("\nFirst five predictions:")

    print(
        prediction_df.head()
    )

    print("\nWeek 9 ML Pipeline completed successfully.")


if __name__ == "__main__":
    main()