from src.extract import extract
from src.transform import transform
from src.validate import validate
from src.load import load


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