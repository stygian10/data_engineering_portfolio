from src.extract import extract_weather_data
from src.transform import transform_weather_data
from src.load import load_weather_data
from src.validate import validate_weather_data


def run_pipeline():
    """
    Execute the complete weather ETL pipeline.
    """

    print("========== WEATHER ETL PIPELINE STARTED ==========")

    extract_weather_data()

    transform_weather_data()

    load_weather_data()

    validate_weather_data()

    print("========== WEATHER ETL PIPELINE COMPLETED ==========")


if __name__ == "__main__":
    run_pipeline()