import pandas as pd

from datetime import datetime

from src.config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
)


def transform_weather_data():
    """
    Transform all raw weather CSV files into cleaned,
    processed weather datasets.
    """

    raw_files = sorted(RAW_DATA_DIR.glob("weather_raw_*.csv"))

    if not raw_files:
        raise FileNotFoundError(
            "[TRANSFORM] No raw weather files found."
        )

    for raw_file in raw_files:

        processed_file = (
            PROCESSED_DATA_DIR
            / raw_file.name.replace("raw", "processed")
        )

        if processed_file.exists():
            print(
                f"[TRANSFORM] Skipping already processed file: "
                f"{raw_file.name}"
            )
            continue

        try:

            df = pd.read_csv(raw_file)

            # Standardize column names
            df.columns = [column.lower() for column in df.columns]

            # Rename Open-Meteo column to match database schema
            df.rename(
                columns={
                    "windspeed_10m": "wind_speed_10m"
                },
                inplace=True,
            )

            # Remove missing values
            df.dropna(inplace=True)

            # Remove unrealistic weather values
            df = df[
                (df["temperature_2m"] > -50)
                & (df["temperature_2m"] < 60)
            ]

            df = df[
                (df["relative_humidity_2m"] >= 0)
                & (df["relative_humidity_2m"] <= 100)
            ]

            # Remove extraction timestamp
            if "extraction_time" in df.columns:
                df.drop(
                    columns=["extraction_time"],
                    inplace=True,
                )

            df.to_csv(processed_file, index=False)

            print(
                f"[TRANSFORM] {raw_file.name} processed successfully."
            )

            print(
                f"Rows: {len(df)} | "
                f"Saved: {processed_file.name}"
            )

        except Exception as error:

            print(
                f"[TRANSFORM] Failed processing "
                f"{raw_file.name}: {error}"
            )

            raise