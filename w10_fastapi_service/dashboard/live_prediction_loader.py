from datetime import datetime
from pathlib import Path
import logging

import pandas as pd

logging.basicConfig(level=logging.INFO)


# Feature dataset paths


DOCKER_FEATURE_PATH = Path(
    "/app/w7_feature_engineering/data/processed/w7_features_final.parquet"
)

LOCAL_FEATURE_PATH = (
    Path(__file__).resolve().parents[2]
    / "w7_feature_engineering"
    / "data"
    / "processed"
    / "w7_features_final.parquet"
)


# Detect execution environment


if DOCKER_FEATURE_PATH.is_file():

    FEATURE_FILE = DOCKER_FEATURE_PATH

    logging.info("Running inside Docker")

else:

    FEATURE_FILE = LOCAL_FEATURE_PATH

    logging.info("Running locally")

logging.info(f"Feature File: {FEATURE_FILE}")



# Load feature dataset


def load_live_prediction_data():
    """
    Load the engineered feature dataset used for
    live predictions.
    """

    if not FEATURE_FILE.exists():

        raise FileNotFoundError(
            f"Feature file not found:\n{FEATURE_FILE}"
        )

    df = pd.read_parquet(FEATURE_FILE)

    df["date"] = pd.to_datetime(df["date"])

    # Reconstruct city from one-hot encoding

    df["city"] = "Edinburgh"

    df.loc[df["city_London"], "city"] = "London"

    df.loc[df["city_Manchester"], "city"] = "Manchester"

    logging.info(
        f"Loaded {len(df)} feature rows."
    )

    return df



# Available cities


def get_available_cities(df):
    """
    Return all available cities.
    """

    return sorted(df["city"].unique())



# City data


def get_city_data(df, city):
    """
    Return all feature records for the selected city.
    """

    return df[
        df["city"] == city
    ].copy()



# Today's feature record


def get_today_record(df, city):
    """
    Return today's engineered feature record.

    Parameters
    ----------
    df : pandas.DataFrame
        Feature dataset.

    city : str
        Selected city.

    Returns
    -------
    pandas.Series
        Today's feature record.

    None
        If today's ETL pipeline has not
        produced today's feature data.
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

    today = datetime.now().date()

    today_df = city_df[
        city_df["date"].dt.date == today
    ]

    if today_df.empty:

        logging.warning(

            f"No feature record found for "

            f"{city} on {today}."

        )

        return None

    logging.info(

        f"Today's feature record found "

        f"for {city}."

    )

    return today_df.iloc[0]



# Validate today's feature record


def validate_today_record(city):
    """
    Validate that today's feature record exists.

    Returns
    -------
    tuple
        (status, message, record)
    """

    df = load_live_prediction_data()

    record = get_today_record(
        df,
        city,
    )

    if record is None:

        return (
            False,
            (
                "Today's feature data is unavailable. "
                "Run today's ETL pipeline before "
                "requesting predictions."
            ),
            None,
        )
    
    print("\nToday's Record")
    print(record)

    return (
        True,
        "Today's feature record is available.",
        record,
    )