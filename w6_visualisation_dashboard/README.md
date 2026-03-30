Airflow DAG: w6_dashboard_refresh
------------------------------------------------
[Trigger W5 Spark ETL] → [Read Parquet from MinIO/W5 output]
            │
            ▼
[Update Dash App / Generate Visuals]
            │
            ▼
[Optional: Push Parquet snapshots to MinIO]
            │
            ▼
[End Pipeline / Logging]

Visualization Dashboard Flow Diagram

             ┌─────────────────────────┐
             │  W5 Spark ETL Output    │
             │  Parquet Files (daily)  │
             └─────────────┬──────────┘
                           │
                           ▼
          ┌─────────────────────────────┐
          │  W6 Dash App (Python + Plotly) │
          │  Reads Parquet / MinIO         │
          │  Generates Multi-city Plots    │
          └─────────────┬───────────────┘
                        │
                        ▼
             ┌───────────────────┐
             │  MinIO / S3       │
             │  Stores Parquet   │
             │  For dashboard & backup │
             └───────────────────┘
                        │
                        ▼
             ┌───────────────────┐
             │  Airflow DAG      │
             │  Automates daily  │
             │  update & refresh │
             └───────────────────┘

            
*****Key Notes for Automation*****
1: Trigger Order:
W4 completes → W5 triggers → Parquet ready → W6 DAG triggers
2: Dashboard Access:
Dockerized Dash app can run as a service or in a container
3: MinIO Integration:
Acts as a production-like data lake
Airflow can pull and push data via boto3 tasks
4: Testing & Validation:
Dash app should read Parquet with same schema as W5
Validate data integrity via sample plots before pushing