import logging
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

logging.basicConfig(level=logging.INFO)

# Feature dataset path

FEATURE_FILE = Path(
    os.getenv(
        "FEATURE_FILE",
        "/workspace/w7_feature_engineering/data/processed/w7_features_final.parquet",
    )
)

logging.info(f"Feature File: {FEATURE_FILE}")

# Columns

TIME_COLUMN = "time"
TARGET_COLUMN = "target_temp_next_hour"


def load_live_prediction_data():
    """
    Load the engineered feature dataset used for
    live prediction.
    """

    if not FEATURE_FILE.exists():
        raise FileNotFoundError(
            f"Feature file not found:\n{FEATURE_FILE}"
        )

    df = pd.read_parquet(FEATURE_FILE)

    df[TIME_COLUMN] = pd.to_datetime(
        df[TIME_COLUMN]
    )

    # Reconstruct city from one-hot encoding

    df["city"] = "Edinburgh"

    df.loc[
        df["city_London"] == 1,
        "city"
    ] = "London"

    df.loc[
        df["city_Manchester"] == 1,
        "city"
    ] = "Manchester"

    logging.info(
        f"Loaded {len(df)} feature rows."
    )

    return df


def get_available_cities(df):
    """
    Return all available cities.
    """

    return sorted(
        df["city"].unique()
    )


def get_city_data(df, city):
    """
    Return all records for one city.
    """

    city_df = df[
        df["city"] == city
    ].copy()

    city_df = city_df.sort_values(
        TIME_COLUMN
    )

    return city_df


def get_latest_record(df, city):
    """
    Return the feature record for the current
    date and hour.
    """

    city_df = get_city_data(
        df,
        city,
    )

    if city_df.empty:
        logging.warning(
            f"No records found for {city}."
        )

        return None

    # Ensure timestamps are hourly

    city_df[TIME_COLUMN] = (
        city_df[TIME_COLUMN]
        .dt.floor("h")
    )

    # Current date and hour

    current_hour = (
        datetime.now(
            ZoneInfo("Europe/London")
        )
        .replace(
            minute=0,
            second=0,
            microsecond=0,
            tzinfo=None,
        )
    )

    # Find today's matching hour

    record = city_df[
        city_df[TIME_COLUMN] == current_hour
    ]

    # If today's hour is missing, use nearest record

    if record.empty:

        logging.warning(
            f"No feature record found for "
            f"{city} at {current_hour}. "
            "Using nearest available record."
        )

        city_df = city_df.copy()

        city_df["time_difference"] = (
            city_df[TIME_COLUMN]
            - current_hour
        ).abs()

        record = city_df.loc[
            [city_df["time_difference"].idxmin()]
        ]

    selected_record = record.iloc[0]

    logging.info(
        f"Selected feature record for {city}: "
        f"{selected_record[TIME_COLUMN]}"
    )

    return selected_record


def validate_latest_record(city):
    """
    Validate that a feature record exists.

    Returns
    -------
    tuple
        (status, message, record)
    """

    df = load_live_prediction_data()

    record = get_latest_record(
        df,
        city,
    )

    if record is None:
        return (
            False,
            (
                "No engineered feature record "
                "is available for the selected city."
            ),
            None,
        )

    return (
        True,
        "Latest feature record loaded successfully.",
        record,
    )


def prepare_api_payload(record):
    """
    Convert a feature record into the payload
    expected by the FastAPI prediction endpoint.
    """

    if record is None:
        return None

    payload = record.drop(
        labels=[
            TIME_COLUMN,
            TARGET_COLUMN,
            "city",
        ]
    ).to_dict()

    # Convert NumPy values into native Python types

    for key, value in payload.items():

        if hasattr(value, "item"):
            payload[key] = value.item()

    print("\n===== FASTAPI PAYLOAD =====")

    for key, value in payload.items():
        print(f"{key}: {value}")

    print("===========================\n")

    return payload