from .load_model import load_model
from .load_features import load_features
from .predict import predict
from .save_predictions import save_predictions
from .evaluate_predictions import evaluate_predictions

# from .upload_to_minio import upload_predictions
# Uploading is handled separately by the Airflow pipeline.


def main():
    """
    Execute the complete Week 9 machine learning inference pipeline.
    """

    try:

        # Load model and scaler
        print("\nLoading trained model and scaler...")

        model, scaler = load_model()

        # Load features
        print("\nLoading feature dataset...")

        features_df = load_features()

        # Generate predictions
        print("\nGenerating predictions...")

        prediction_df = predict(
            model,
            scaler,
            features_df,
        )

        # Evaluate predictions
        print("\nEvaluating predictions...")

        metrics = evaluate_predictions(
            prediction_df,
        )

        # Save predictions
        print("\nSaving prediction files...")

        save_predictions(
            prediction_df,
        )

        # Upload handled by Airflow
        # print("\nUploading prediction files to MinIO...")
        # upload_predictions()

        # Pipeline summary

        print("\n" + "=" * 60)
        print("WEEK 9 PIPELINE SUMMARY")
        print("=" * 60)

        print(f"Prediction Records : {len(prediction_df)}")
        print(f"MAE                : {metrics['MAE']:.2f}")
        print(f"RMSE               : {metrics['RMSE']:.2f}")
        print(f"R²                 : {metrics['R2']:.2f}")

        print("\nFirst Five Predictions")

        print(
            prediction_df.head()
        )

        print("\nWeek 9 ML Pipeline completed successfully.")

    except Exception as error:

        print("\nPipeline failed.")

        print(error)

        raise


if __name__ == "__main__":
    main()