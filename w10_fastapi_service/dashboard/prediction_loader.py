from pathlib import Path
import logging

import pandas as pd

logging.basicConfig(level=logging.INFO)

# Prediction file locations

DOCKER_PREDICTION_PATH = Path(
    "/app/w9_ml_pipeline/data/predictions/weather_predictions.csv"
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

    # Convert date column

    df["date"] = pd.to_datetime(df["date"])

    # Remove today's predictions
    # Historical data should only contain previous days

    from datetime import datetime

    today = datetime.now().date()

    df = df[df["date"].dt.date < today
    
    ]

    # Reconstruct city names from one-hot encoding

    df["city"] = "Edinburgh"

    df.loc[df["city_London"], "city"] = "London"
    df.loc[df["city_Manchester"], "city"] = "Manchester"

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
        df["date"]
        .sort_values()
        .dt.strftime("%Y-%m-%d")
        .tolist()
    )


def filter_city_data(df, city):
    """
    Return the complete prediction history
    for the selected city.

    Used by charts and tables.
    """

    return df[df["city"] == city].copy()


def filter_prediction_data(df, city, selected_date):
    """
    Return a single prediction record.

    Used by KPI cards.
    """

    filtered_df = filter_city_data(df, city)

    if selected_date:

        filtered_df = filtered_df[
            filtered_df["date"] == pd.to_datetime(selected_date)
        ]

    return filtered_df