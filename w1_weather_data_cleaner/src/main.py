from download import download_historical_data
from clean import clean_weather_data


def run_pipeline():
    download_historical_data()
    clean_weather_data()


def main():
    run_pipeline()


if __name__ == "__main__":
    main()