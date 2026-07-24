from pathlib import Path
from datetime import datetime
import logging

import pandas as pd

logging.basicConfig(level=logging.INFO)

# Prediction file locations

DOCKER_PREDICTION_PATH = Path(
    "/workspace/w9_ml_pipeline/data/predictions/weather_predictions.csv"
)

LOCAL_PREDICTION_PATH = (
    Path(__file__).resolve().parents[2]
    / "w9_ml_pipeline"
    / "data"
    / "predictions"
    / "weather_predictions.csv"
)

# Detect execution environment

if DOCKER_PREDICTION_PATH.is_file():
    PREDICTION_FILE = DOCKER_PREDICTION_PATH
    logging.info("Running inside Docker")
else:
    PREDICTION_FILE = LOCAL_PREDICTION_PATH
    logging.info("Running locally")

logging.info(f"Prediction File: {PREDICTION_FILE}")


def load_prediction_data():
    """Load the Week 9 prediction dataset."""

    if not PREDICTION_FILE.exists():
        raise FileNotFoundError(
            f"Prediction file not found:\n{PREDICTION_FILE}"
        )

    df = pd.read_csv(PREDICTION_FILE)

    # Convert timestamp column

    df["time"] = pd.to_datetime(df["time"])

    # Remove today's predictions
    # Historical data should only contain previous days

    today = datetime.now().date()

    df = df[df["time"].dt.date < today]

    # Reconstruct city names from one-hot encoding

    df["city"] = "Edinburgh"

    df.loc[df["city_London"] == 1, "city"] = "London"
    df.loc[df["city_Manchester"] == 1, "city"] = "Manchester"

    logging.info(f"Loaded {len(df)} prediction rows.")


    return df


def get_available_cities(df):
    """Return all available cities."""

    return sorted(df["city"].unique())


def get_city_data(df, city):
    """Return all records for a city."""

    return df[df["city"] == city].copy()


def get_available_dates(df):
    """Return all available dates."""

    return (
        df["time"]
        .dt.strftime("%Y-%m-%d")
        .sort_values()
        .unique()
        .tolist()
    )


def filter_city_data(df, city):
    """
    Return the complete prediction history
    for the selected city.

    Used by charts and tables.
    """

    return df[df["city"] == city].copy()


def filter_prediction_data(df, city, selected_date=None):
    """
    Return prediction history for the selected city.
    Optionally filter by a specific date.
    """

    filtered_df = filter_city_data(df, city)

    if selected_date:

        selected_date = pd.to_datetime(selected_date).date()

        filtered_df = filtered_df[
            filtered_df["time"].dt.date == selected_date
        ]

    return filtered_df