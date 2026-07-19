import logging
from datetime import datetime, timedelta

import pandas as pd
import requests

from config import (
    API_URL,
    CITIES,
    HOURLY_VARIABLES,
    RAW_DATA_DIR,
    RAW_DATA_FILE,
    REQUEST_TIMEOUT,
    START_DATE,
    TIMEZONE,
)


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
)


def get_end_date():
    """
    Returns yesterday's date.
    """

    return (
        datetime.today() - timedelta(days=1)
    ).strftime("%Y-%m-%d")


def build_request_params(city):
    """
    Builds the API request parameters for one city.
    """

    return {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "start_date": START_DATE,
        "end_date": get_end_date(),
        "hourly": ",".join(HOURLY_VARIABLES),
        "timezone": TIMEZONE,
    }


def download_city_data(city):
    """
    Downloads historical weather for one city.
    """

    logging.info("Downloading %s...", city["name"])

    response = requests.get(
        API_URL,
        params=build_request_params(city),
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    weather_json = response.json()

    if "hourly" not in weather_json:
        raise ValueError(
            f"No hourly data returned for {city['name']}"
        )

    city_dataframe = pd.DataFrame(
        weather_json["hourly"]
    )

    city_dataframe["city"] = city["name"]

    logging.info(
        "%s: %s rows downloaded",
        city["name"],
        len(city_dataframe),
    )

    return city_dataframe


def download_historical_data():
    """
    Downloads historical weather data for all cities.
    """

    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    all_data = []

    for city in CITIES:
        city_data = download_city_data(city)
        all_data.append(city_data)

    weather_dataframe = pd.concat(
        all_data,
        ignore_index=True,
    )

    weather_dataframe.to_csv(
        RAW_DATA_FILE,
        index=False,
    )

    logging.info("----------------------------------------")
    logging.info("Historical download completed")
    logging.info("Rows downloaded : %s", len(weather_dataframe))
    logging.info("Cities          : %s", len(CITIES))
    logging.info("Start Date      : %s", START_DATE)
    logging.info("End Date        : %s", get_end_date())
    logging.info("Saved File      : %s", RAW_DATA_FILE)
    logging.info("----------------------------------------")

    return weather_dataframe


def main():

    download_historical_data()


if __name__ == "__main__":
    main()