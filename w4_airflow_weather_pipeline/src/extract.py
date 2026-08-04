import requests
import pandas as pd

from datetime import datetime

from src.config import (
    OPEN_METEO_URL,
    CITIES,
    HOURLY_VARIABLES,
    TIMEZONE,
    REQUEST_TIMEOUT,
    RAW_DATA_DIR,
)


def extract_weather_data():
    """
    Extract today's hourly weather forecast data from Open-Meteo
    for all configured cities and save each city as a raw CSV.

    Returns
    -------
    list
        List of generated CSV file paths.
    """

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    today = datetime.utcnow().strftime("%Y-%m-%d")

    output_files = []

    for city, coordinates in CITIES.items():

        params = {
            "latitude": coordinates["latitude"],
            "longitude": coordinates["longitude"],
            "hourly": HOURLY_VARIABLES,
            "timezone": TIMEZONE,
            "start_date": today,
            "end_date": today,
        }

        try:

            response = requests.get(
                OPEN_METEO_URL,
                params=params,
                timeout=REQUEST_TIMEOUT,
            )

            response.raise_for_status()

            data = response.json()

            hourly_data = data.get("hourly")

            if not hourly_data:
                print(
                    f"[EXTRACT] No hourly weather data returned for {city}"
                )
                continue

            df = pd.DataFrame(hourly_data)

            df["extraction_time"] = datetime.utcnow()

            output_file = (
                RAW_DATA_DIR
                / f"weather_raw_{city}_{timestamp}.csv"
            )

            df.to_csv(output_file, index=False)

            output_files.append(str(output_file))

            print(
                f"[EXTRACT] {city} completed | "
                f"Rows: {len(df)} | "
                f"Saved: {output_file.name}"
            )

        except Exception as error:

            print(f"[EXTRACT] Failed for {city}: {error}")
            raise

    return output_files