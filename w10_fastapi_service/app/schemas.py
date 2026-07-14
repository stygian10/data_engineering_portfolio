# Defines request/response models
from pydantic import BaseModel


class WeatherFeatures(BaseModel):
    temperature: float
    temp_max: float
    temp_min: float
    humidity: float
    windspeed: float
    rolling_avg_temp: float

    day_of_week: int
    month: int
    week_of_year: int

    temp_rolling_mean: float
    humidity_rolling_mean: float
    windspeed_rolling_mean: float

    temp_lag_1: float
    temp_lag_3: float
    humidity_lag_1: float
    windspeed_lag_1: float

    temp_delta: float
    humidity_delta: float
    windspeed_delta: float

    temp_pct_change: float
    humidity_pct_change: float
    windspeed_pct_change: float

    city_London: bool
    city_Manchester: bool


class PredictionResponse(BaseModel):
    predicted_temperature: float