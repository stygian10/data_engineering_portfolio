import logging

import pandas as pd

from src.config import (
    PROCESSED_DATA_DIR,
    PROCESSED_DATA_FILE,
    RAW_DATA_FILE,
)

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
)


def clean_weather_data():
    """
    Cleans the historical weather dataset.
    """

    logging.info("Loading raw weather data...")

    df = pd.read_csv(RAW_DATA_FILE)

    logging.info("Rows loaded: %s", len(df))

    # Convert time column to datetime
    df["time"] = pd.to_datetime(df["time"])

    # Remove duplicate rows
    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:
        logging.info(
            "Removing %s duplicate rows...",
            duplicate_count,
        )

        df = df.drop_duplicates()

    # Sort by time then city
    df = (
        df.sort_values(
            by=["time", "city"]
        )
        .reset_index(drop=True)
    )

    logging.info(
        "Date Range     : %s -> %s",
        df["time"].min(),
        df["time"].max(),
    )

    logging.info(
        "Cities         : %s",
        ", ".join(
            sorted(df["city"].unique())
        ),
    )

    # Create processed directory if it doesn't exist
    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Save cleaned dataset
    df.to_csv(
        PROCESSED_DATA_FILE,
        index=False,
    )

    logging.info("----------------------------------------")
    logging.info("Cleaning completed")
    logging.info("Rows           : %s", len(df))
    logging.info("Columns        : %s", len(df.columns))
    logging.info("Duplicates     : %s", duplicate_count)
    logging.info(
        "Missing Values : %s",
        df.isnull().sum().sum(),
    )
    logging.info(
        "Saved File     : %s",
        PROCESSED_DATA_FILE,
    )
    logging.info("----------------------------------------")

    return df


def main():

    clean_weather_data()


if __name__ == "__main__":
    main()