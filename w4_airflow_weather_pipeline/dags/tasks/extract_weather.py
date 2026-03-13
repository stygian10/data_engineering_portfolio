import requests
import pandas as pd
from datetime import datetime
from pathlib import Path

def extract_weather_data():
    """
    Extract hourly weather data for London, Manchester, and Edinburgh
    from Open-Meteo API and save each as a raw CSV file.

    Returns a list of file paths for downstream Airflow tasks (XCom-friendly).
    """

    # -----------------------------
    # Cities configuration
    # -----------------------------
    cities = {
        "London": {"latitude": 51.5072, "longitude": -0.1276},
        "Manchester": {"latitude": 53.4808, "longitude": -2.2426},
        "Edinburgh": {"latitude": 55.9533, "longitude": -3.1883}
    }

    # -----------------------------
    # Output path (Airflow volume)
    # -----------------------------
    output_dir = Path("/opt/airflow/data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    output_files = []  # to store paths for XCom

    # -----------------------------
    # Loop through cities and extract data
    # -----------------------------
    for city, coords in cities.items():
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": coords["latitude"],
            "longitude": coords["longitude"],
            "hourly": [
                "temperature_2m",
                "relativehumidity_2m",
                "windspeed_10m"
            ],
            "timezone": "UTC"
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            hourly_data = data.get("hourly")
            if not hourly_data:
                print(f"[EXTRACT] Warning: No hourly data returned for {city}")
                continue

            # -----------------------------
            # Convert to DataFrame
            # -----------------------------
            df = pd.DataFrame(hourly_data)

            # Add extraction timestamp
            df["extraction_time"] = datetime.utcnow()

            # Save CSV
            output_file = output_dir / f"weather_raw_{city}_{timestamp}.csv"
            df.to_csv(output_file, index=False)
            output_files.append(str(output_file))  # store path for XCom

            # Logging
            print(f"[EXTRACT {datetime.utcnow()}] {city} weather data extraction completed")
            print(f"Rows extracted: {len(df)} | File saved to: {output_file}")

        except Exception as e:
            print(f"[EXTRACT] Failed to extract data for {city}: {e}")
            raise

    return output_files  # return list of file paths for downstream tasks