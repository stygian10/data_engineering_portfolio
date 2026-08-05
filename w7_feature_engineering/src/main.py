from .load_data import (
    download_from_minio,
    load_data
)

from .features import run_feature_pipeline

from .config import OUTPUT_DATA_PATH


def save_data(df):
    """
    Save the final ML-ready feature dataset.
    """

    if OUTPUT_DATA_PATH.exists():
        OUTPUT_DATA_PATH.unlink()

        print("Removed old processed dataset.")

    df.to_parquet(
        OUTPUT_DATA_PATH,
        index=False
    )

    print("\nFeature dataset saved successfully.")
    print(f"Output File:\n{OUTPUT_DATA_PATH}")


def main():
    """
    Execute the complete Week 7 feature engineering pipeline.
    """

    print("Downloading latest weather dataset from MinIO...")

    parquet_file = download_from_minio()

    print("\nLoading weather dataset...")

    weather_df = load_data(parquet_file)

    print("\nRunning feature engineering pipeline...")

    feature_df = run_feature_pipeline(weather_df)

    print("\nSaving feature dataset...")

    save_data(feature_df)

    print("\nPipeline completed successfully.")

    print(f"\nRows: {len(feature_df)}")
    print(f"Columns: {len(feature_df.columns)}")

    print("\nColumns:")
    print(feature_df.columns.tolist())

    print("\nFirst five rows:")
    print(feature_df.head())


if __name__ == "__main__":
    main()