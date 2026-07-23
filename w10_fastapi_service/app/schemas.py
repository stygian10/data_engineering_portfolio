from pydantic import BaseModel


class PredictionRequest(BaseModel):
    temperature: float
    humidity: float
    windspeed: float

    year: int
    month: int
    day: int
    hour: int
    day_of_week: int
    week_of_year: int
    day_of_year: int
    is_weekend: int

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

    city_London: int
    city_Manchester: int

    source_forecast: int


class PredictionResponse(BaseModel):
    predicted_temperature: float