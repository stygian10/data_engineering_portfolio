from load_model import load_model
from load_features import load_features
from predict import predict
from save_predictions import save_predictions
# from upload_to_minio import upload_predictions
""" disabling the upload functions as there will be a seprate 
upload function in the airflow for simplicity and and efficiancy"""


def main():
    """
    Execute the weather prediction inference pipeline.
    """

    # Load the trained model
    print("Loading trained model...")

    model = load_model()

    # Load the feature dataset
    print("\nLoading feature dataset...")

    features_df = load_features()

    # Generate predictions
    print("\nGenerating predictions...")

    prediction_df = predict(model, features_df)

    # Save prediction files
    print("\nSaving prediction files...")

    save_predictions(prediction_df)

    # Uploading prediction files to Mini0 

    #print("\nUploading prediction files to MinIO...")

    #upload_predictions()

    # Display summary
    print("\nPrediction Summary")

    print(f"Prediction Records: {len(prediction_df)}")

    # Display sample predictions
    print("\nFirst five predictions:")

    print(prediction_df.head())


if __name__ == "__main__":
    main()