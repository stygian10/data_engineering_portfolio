from pathlib import Path
import logging

import requests 

logging.basicConfig(level=logging.INFO)

# FastAPI endpoints

DOCKER_API_URL = "http://fastapi:8000/predict"

LOCAL_API_URL = "http://127.0.0.1:8000/predict"

# Detect execution environment

if Path("/.dockerenv").exists():

    API_URL = DOCKER_API_URL

    logging.info("Running inside Docker")

else:

    API_URL = LOCAL_API_URL

    logging.info("Running locally")

logging.info(f"FastAPI Endpoint: {API_URL}")

#JSON Payload

def build_payload(row):
    """
    Convert a prediction record into the
    JSON payload expected by the FastAPI
    prediction endpoint.
    """

    payload = {

        "temperature": float(row["temperature"]),
        "temp_max": float(row["temp_max"]),
        "temp_min": float(row["temp_min"]),

        "humidity": float(row["humidity"]),
        "windspeed": float(row["windspeed"]),

        "rolling_avg_temp": float(row["rolling_avg_temp"]),

        "day_of_week": int(row["day_of_week"]),
        "month": int(row["month"]),
        "week_of_year": int(row["week_of_year"]),

        "temp_rolling_mean": float(row["temp_rolling_mean"]),
        "humidity_rolling_mean": float(row["humidity_rolling_mean"]),
        "windspeed_rolling_mean": float(row["windspeed_rolling_mean"]),

        "temp_lag_1": float(row["temp_lag_1"]),
        "temp_lag_3": float(row["temp_lag_3"]),

        "humidity_lag_1": float(row["humidity_lag_1"]),
        "windspeed_lag_1": float(row["windspeed_lag_1"]),

        "temp_delta": float(row["temp_delta"]),
        "humidity_delta": float(row["humidity_delta"]),
        "windspeed_delta": float(row["windspeed_delta"]),

        "temp_pct_change": float(row["temp_pct_change"]),
        "humidity_pct_change": float(row["humidity_pct_change"]),
        "windspeed_pct_change": float(row["windspeed_pct_change"]),

        "city_London": bool(row["city_London"]),
        "city_Manchester": bool(row["city_Manchester"]),
    }

    return payload

# Handle JSON Response & Send HTTP POST request, error handling

def request_prediction(row):
    """
    Send a prediction request to the FastAPI service
    and return the predicted temperature.
    """

    try:

        payload = build_payload(row)

        response = requests.post(
            API_URL,
            json=payload,
            timeout=10,
        )

        response.raise_for_status()

        prediction = response.json()

        return prediction

    except requests.exceptions.ConnectionError:

        logging.error(
            "Unable to connect to the FastAPI service."
        )

        return None

    except requests.exceptions.Timeout:

        logging.error(
            "The request to the FastAPI service timed out."
        )

        return None

    except requests.exceptions.HTTPError as error:

        logging.error(
            f"HTTP Error: {error}"
        )

        return None

    except requests.exceptions.RequestException as error:

        logging.error(
            f"Request Error: {error}"
        )

        return None

    except Exception as error:

        logging.exception(
            f"Unexpected Error: {error}"
        )

        return None

