# Week 8 — Weather Prediction Model

## Project Overview

The goal of Week 8 is to develop, evaluate and deploy a machine learning model capable of predicting the next day's average temperature using the engineered weather dataset produced in Week 7.

The project evaluates multiple regression algorithms, compares their performance, and selects the best-performing model for inference.

The final output is a serialised production-ready machine learning model that can be reused for future predictions without retraining.

# Project Goal

The primary objective of this project is to:

- load the ML-ready dataset from Week 7,
- train baseline and advanced regression models,
- compare model performance,
- evaluate prediction accuracy,
- select the best-performing model,
- serialize the selected model,
- generate predictions using the latest weather features.

The project simulates a production-style machine learning workflow commonly used in:

- machine learning engineering,
- predictive analytics,
- forecasting systems,
- production model deployment.

# Pipeline Architecture

Week 7 Feature Dataset

↓

Model Training

↓

Linear Regression

↓

Random Forest

↓

Model Evaluation

↓

Best Model Selection

↓

Model Serialization

↓

Prediction Pipeline