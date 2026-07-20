from extract import extract
from transform import transform
from validate import validate
from load import load


def run_pipeline():
    """
    Run the complete ETL pipeline.
    """

    print("\n===== W2 Weather ETL Pipeline =====\n")

    df = extract()
    df = transform(df)
    df = validate(df)
    load(df)

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()