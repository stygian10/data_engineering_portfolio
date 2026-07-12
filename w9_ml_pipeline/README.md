# Week 9 – ML Inference Pipeline

## Objective

Build an automated machine learning inference pipeline that loads a trained weather prediction model, generates batch predictions from engineered features, evaluates prediction quality, saves prediction datasets, and integrates with Apache Airflow for automated execution.

--

## Workflow
Load Trained Model
↓
Load Engineered Features
↓
Generate Predictions
↓
Evaluate Predictions
↓
Save CSV & Parquet
↓
Upload Predictions to MinIO (Airflow Task)

---

## Project Strcuture

├── README.md
├── data
│   └── predictions
├── figures
│   ├── error_distribution.png
│   ├── prediction_vs_actual.png
│   └── residual_plot.png
└── src
    ├── config.py
    ├── evaluate_predictions.py
    ├── load_features.py
    ├── load_model.py
    ├── main.py
    ├── predict.py
    ├── save_predictions.py
    └── upload_to_minio.py

--- 

## Project Outputs

The pipeline produces:

- Weather prediction dataset (CSV)
- Weather prediction dataset (Parquet)
- Prediction vs Actual visualization
- Residual Plot
- Error Distribution Plot

---

## Prediction Evaluation Summary

The prediction pipeline was evaluated using the engineered feature dataset generated in Week 7 and the Linear Regression model trained in Week 8.

### Performance Metrics

| Metric | Result | 
|---------|--------|
| Mean Absolute Error (MAE) | **1.23°C** |
| Root Mean Squared Error (RMSE) | **1.79°C** |
| R² Score | **0.91** |

Visual evaluation showed a strong linear relationship between the actual and predicted temperatures. Residuals were centered around zero with no obvious systematic pattern, indicating consistent model performance.

Overall, the inference pipeline produces accurate weather forecasts suitable for automated batch prediction within the Weather Intelligence Platform.

---

## Status

**Completed** 