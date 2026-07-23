import logging

import requests


logging.basicConfig(level=logging.INFO)


# FastAPI endpoint

API_URL = "http://fastapi:8000/predict"


def request_prediction(payload):
    """
    Send a prediction request to the FastAPI service.

    Parameters
    ----------
    payload : dict
        Feature dictionary prepared from the
        latest W7 feature record.

    Returns
    -------
    float
        Predicted temperature.

    Raises
    ------
    RuntimeError
        If the API request fails.
    """

    try:

        response = requests.post(
            API_URL,
            json=payload,
            timeout=10,
        )

        response.raise_for_status()

    except requests.exceptions.RequestException as exc:

        logging.error(
            f"Prediction request failed: {exc}"
        )

        raise RuntimeError(
            "Unable to connect to the prediction service."
        ) from exc

    result = response.json()

    if "predicted_temperature" not in result:

        raise RuntimeError(
            "Prediction response is missing "
            "'predicted_temperature'."
        )

    prediction = result["predicted_temperature"]

    logging.info(
        f"Prediction received: {prediction:.2f} °C"
    )

    return prediction


def check_api_health():
    """
    Check whether the FastAPI service is running.

    Returns
    -------
    bool
        True if the API is reachable.
    """

    try:

        response = requests.get(
            "http://fastapi:8000/",
            timeout=5,
        )

        return response.status_code == 200

    except requests.exceptions.RequestException:

        return False