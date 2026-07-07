from load_model import load_model
from load_features import load_features
from predict import predict


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

    # Display summary
    print("\nPrediction Summary")

    print(f"Total predictions: {len(prediction_df)}")

    # Display sample predictions
    print("\nFirst five predictions:")

    print(prediction_df.head())


if __name__ == "__main__":
    main()