# Data Engineering Portfolio Project

## Overview
End-to-end data engineering and ML pipeline built across 12 weeks.

## Pipeline Flow
API → Airflow → Spark → MinIO → Dashboard → Feature Engineering → ML → API

## Projects

| Week | Module                 |
|------|----------------------- |
| W1   | Data Cleaning          |
| W2   | ETL Pipeline           |
| W3   | PostgreSQL Loader      |
| W4   | Airflow Orchestration  |
| W5   | Spark ETL              |
| W6   | Dashboard + Data Lake  |
| W7   | Feature Engineering    |
| W8   | Machine Learning Model |
| W9   | Model API              |
| W10  | Full Orchestration     |
| W11  | Documentation          |
| W12  | Deployment             |
---------------------------------
## Current Stage
 Completed: W1–W10 
🚧 In Progress: W11 (Model API)

## Tech Stack
Python, Pandas, PySpark, Airflow, Docker, MinIO (S3), PostgreSQL, Scikit-learn, Flask

                      Historical Pipeline (Runs Once)
                                W1 → W2 → W3
                                    │
                                    ▼
                          Historical Database
                                    │
                                    ▼
                     Daily Pipeline (Runs Every Day)
                    W4 → W5 → W6 → W7 → W8 → W9 → W10