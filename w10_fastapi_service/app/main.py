from fastapi import FastAPI

from app.routes import router


app = FastAPI(
    title="Weather Prediction API",
    description=(
        "FastAPI service for predicting the next-hour "
        "temperature using the Week 8 trained "
        "Linear Regression model."
    ),
    version="1.0.0",
)


app.include_router(router)