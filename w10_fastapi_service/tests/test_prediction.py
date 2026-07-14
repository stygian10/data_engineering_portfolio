import pandas as pd
import requests
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

PREDICTION_FILE = (
    BASE_DIR
    / "w9_ml_pipeline"
    / "data"
    / "predictions"
    / "weather_predictions.csv"
)

API_URL = "http://127.0.0.1:8000/predict"


def main():

    print("=" * 60)
    print("FASTAPI PREDICTION VALIDATION")
    print("=" * 60)

    df = pd.read_csv(PREDICTION_FILE)

    print(f"\nRows Loaded : {len(df)}")

    test_row = df.iloc[0]

    expected_prediction = float(
        test_row["predicted_temperature"]
    )

    feature_columns = [
        "temperature",
        "temp_max",
        "temp_min",
        "humidity",
        "windspeed",
        "rolling_avg_temp",
        "day_of_week",
        "month",
        "week_of_year",
        "temp_rolling_mean",
        "humidity_rolling_mean",
        "windspeed_rolling_mean",
        "temp_lag_1",
        "temp_lag_3",
        "humidity_lag_1",
        "windspeed_lag_1",
        "temp_delta",
        "humidity_delta",
        "windspeed_delta",
        "temp_pct_change",
        "humidity_pct_change",
        "windspeed_pct_change",
        "city_London",
        "city_Manchester",
    ]

    payload = {}

    for column in feature_columns:

        value = test_row[column]

        if column.startswith("city_"):
            payload[column] = bool(value)
        elif column in [
            "day_of_week",
            "month",
            "week_of_year",
        ]:
            payload[column] = int(value)
        else:
            payload[column] = float(value)

    response = requests.post(
        API_URL,
        json=payload,
        timeout=10
    )

    print("\nStatus Code :", response.status_code)

    if response.status_code != 200:
        print(response.text)
        return

    api_prediction = response.json()["predicted_temperature"]

    difference = abs(
        api_prediction -
        expected_prediction
    )

    print("\nExpected Prediction :", expected_prediction)
    print("API Prediction      :", api_prediction)
    print("Difference          :", difference)

    tolerance = 1e-6

    if difference < tolerance:
        print("\nPASS")
        print("FastAPI matches Week 9 predictions.")
    else:
        print("\nFAIL")
        print("Prediction mismatch detected.")


if __name__ == "__main__":
    main()