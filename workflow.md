                                    Open-Meteo API
                                           │
                                           ▼
                              Week 4 Airflow Orchestrator
                                           │
             ┌─────────────────────────────┼─────────────────────────────┐
             │                             │                             │
             ▼                             ▼                             ▼
     Week 1 Historical Data        Weather Forecast API          Pipeline Scheduling
       Collection Module              Collection                     Monitoring
             │
             ▼
     Historical Weather CSV
             │
             ▼
──────────────────────────────────────────────────────────────────────────────

                        Week 2 ETL Data Processing
              Cleaning • Validation • Standardisation • Transformation
                                   │
                                   ▼
                        Processed Weather Dataset
                                   │
                                   ▼
──────────────────────────────────────────────────────────────────────────────

                   Week 3 PostgreSQL Data Warehouse
                     Historical Weather Database
                                   │
                                   ▼
──────────────────────────────────────────────────────────────────────────────

                  Week 4 Airflow Weather Pipeline
      Daily Forecast Download + ETL + Automated Orchestration
                                   │
                                   ▼
                Processed Forecast Dataset (CSV)
                                   │
                                   ▼
──────────────────────────────────────────────────────────────────────────────

                     Week 5 Spark ETL Pipeline
          PySpark Processing + Feature Aggregation + Parquet
                                   │
                                   ▼
                        Partitioned Parquet Files
                                   │
                                   ▼
──────────────────────────────────────────────────────────────────────────────

            Week 6 Object Storage + Interactive Dashboard

                      ┌─────────────────────────┐
                      │        MinIO            │
                      │ Weather Data Lake       │
                      └──────────┬──────────────┘
                                 │
                                 ▼
                     Plotly Dash Visualization
                                 │
                                 ▼
──────────────────────────────────────────────────────────────────────────────

                Week 7 Feature Engineering Pipeline

           Download Parquet from MinIO
                      │
                      ▼
      Feature Engineering + ML Feature Creation
                      │
                      ▼
           w7_features_final.parquet
                      │
                      ▼
──────────────────────────────────────────────────────────────────────────────

               Week 8 Machine Learning Pipeline

      Feature Dataset
            │
            ▼
  Train/Test Split
            │
            ▼
 Compare Multiple Models
            │
            ▼
 Select Best Model
            │
            ├──────────────► model_metrics.json
            │
            ├──────────────► Evaluation Charts
            │
            ▼
      best_model.pkl
            │
            ▼
──────────────────────────────────────────────────────────────────────────────

             Week 9 ML Batch Prediction Pipeline

      Feature Dataset
            │
            ▼
      Load Best Model
            │
            ▼
 Batch Prediction
            │
            ▼
weather_predictions.csv
            │
            ▼
──────────────────────────────────────────────────────────────────────────────

           Week 10 Model Serving + Dashboard Integration

                     Plotly Dash Dashboard
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
      Historical Predictions         Live Prediction
      weather_predictions.csv      Latest Feature Record
                 │                           │
                 │                           ▼
                 │                    FastAPI Prediction API
                 │                           │
                 └──────────────► Best ML Model
                                            │
                                            ▼
                               Real-time Temperature Prediction




                                Complete Data Flow



Open-Meteo API
      │
      ▼
Week 1 Historical Collection
      │
      ▼
Week 2 ETL
      │
      ▼
Week 3 PostgreSQL
      │
      ▼
Week 4 Airflow Automation
      │
      ▼
Week 5 Spark ETL
      │
      ▼
Week 6 MinIO + Dashboard
      │
      ▼
Week 7 Feature Engineering
      │
      ▼
Week 8 Machine Learning
      │
      ├────────► best_model.pkl
      └────────► model_metrics.json
                 │
                 ▼
Week 9 Batch Prediction
      │
      ▼
weather_predictions.csv
      │
      ├────────► Historical Dashboard
      │
      └────────► Week 10 FastAPI
                     ▲
                     │
        Latest Week 7 Features
                     │
                     ▼
            Live Dashboard Prediction