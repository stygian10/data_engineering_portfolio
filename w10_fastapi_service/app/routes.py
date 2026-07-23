import logging

from fastapi import APIRouter, HTTPException

from app.predictor import predict
from app.schemas import (
    PredictionRequest,
    PredictionResponse,
)


logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.get(
    "/",
    tags=["Health"],
)
def health_check():
    """
    Verify that the prediction API is running.
    """

    logging.info("Health check requested.")

    return {
        "status": "online",
        "message": "Weather Prediction API is running.",
    }


@router.post(
    "/predict",
    response_model=PredictionResponse,
    tags=["Prediction"],
)
def predict_temperature(
    request: PredictionRequest,
):
    """
    Predict the next-hour temperature using the
    trained weather prediction model.
    """

    try:

        logging.info(
            "Prediction request received."
        )

        prediction = predict(
            request.model_dump()
        )

        logging.info(
            f"Prediction completed: {prediction:.2f} °C"
        )

        return PredictionResponse(
            predicted_temperature=round(
                prediction,
                2,
            )
        )

    except ValueError as exc:

        logging.exception(
            "Invalid prediction request."
        )

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except FileNotFoundError:

        logging.exception(
            "Model file not found."
        )

        raise HTTPException(
            status_code=500,
            detail="Trained model could not be loaded.",
        )

    except Exception:

        logging.exception(
            "Unexpected prediction error."
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "An unexpected error occurred "
                "while generating the prediction."
            ),
        )