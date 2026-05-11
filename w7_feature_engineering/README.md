# Week 7 — Feature Engineering Pipeline

## Project Overview

The goal of Week 7 is to transform processed weather data into an ML-ready feature dataset for predictive modeling.

The pipeline uses:
- Python
- Pandas
- MinIO (S3-compatible object storage)
- Parquet datasets
- Scikit-learn preprocessing techniques

The final output is a reusable, production-style feature engineering pipeline designed for future machine learning workflows.

---

# Project Goal

The primary objective of this project is to:

- ingest processed weather data from MinIO,
- perform data exploration and validation,
- engineer predictive time-series features,
- prepare a clean ML-ready dataset,
- generate a target variable for forecasting,
- support future model training in Week 8.

The pipeline is designed to simulate a real-world preprocessing workflow commonly used in:
- data engineering,
- ML engineering,
- forecasting systems,
- analytics platforms.

---

# Pipeline Architecture

MinIO Weather Data Lake -> Parquet Data Download -> Data Exploration & Validation -> Feature Engineering Pipeline -> Scaling & Cleaning -> ML-Ready Dataset -> Week 8 Machine Learning Models
