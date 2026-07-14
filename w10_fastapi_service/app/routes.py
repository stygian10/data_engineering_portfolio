# Defines the API endpoints

from fastapi import APIRouter

from app.schemas import (
    WeatherFeatures,
    PredictionResponse,
)

from app.predictor import predict

router = APIRouter()


@router.get("/")
def root():

    return {
        "message": "Weather Prediction API"
    }


@router.get("/health")
def health():

    return {
        "status": "healthy"
    }


@router.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict_temperature(
    weather: WeatherFeatures,
):

    prediction = predict(
        weather.model_dump()
    )

    return PredictionResponse(
        predicted_temperature=prediction
    )