from pathlib import Path

from dotenv import load_dotenv

load_dotenv(
    Path(__file__).resolve().parents[2] / ".env"
)

from src.download import download_historical_data
from src.clean import clean_weather_data


def run_pipeline():
    """
    Execute the complete Week 1 historical data pipeline.
    """

    print("\n===== W1 Historical Weather Pipeline =====\n")

    download_historical_data()

    clean_weather_data()

    print(
        "\n===== W1 Pipeline Completed Successfully ====="
    )


def main():

    run_pipeline()


if __name__ == "__main__":
    main()