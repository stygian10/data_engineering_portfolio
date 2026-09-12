# Weather Intelligence Platform

An end-to-end data engineering and machine learning platform for collecting, processing, storing, analysing, and serving weather data.

The project started as a data engineering and machine learning pipeline and was progressively extended with containerisation, workflow orchestration, object storage, Kubernetes, Oracle Cloud, and CI/CD.

---

## Overview

The platform covers the main stages of a production-style data and ML workflow:

- Weather data collection and cleaning
- ETL and data validation
- PostgreSQL data storage
- Apache Airflow workflow orchestration
- PySpark ETL and Spark SQL analysis
- MinIO S3-compatible object storage
- Amazon S3 cloud artifact storage
- Feature engineering
- Machine learning model comparison, training, and evaluation
- Batch prediction (generating predictions for a prepared dataset in one processing run)
- FastAPI prediction serving
- Plotly Dash prediction dashboard
- Docker and Docker Compose
- Kubernetes and K3s
- Persistent storage with Kubernetes PVCs
- Kubernetes Secrets and RBAC
- Oracle Cloud deployment
- GitHub Actions CI/CD
- GitHub Container Registry
- Immutable commit-SHA container images
- Multi-platform AMD64/ARM64 image builds
- Automated deployment and Kubernetes rollout

The project is divided into two layers:

```text
Phase 1
W1 → W2 → W3 → W4 → W5 → W6 → W7 → W8 → W9 → W10 → W11
Data Engineering + ML + Application

                         ↓

Phase 2
Kubernetes → Platform Consolidation → Cloud → CI/CD
                         ↓
              Public Deployment
                         ↓
             MLflow + Optimisation
                         ↓
              Testing + Monitoring
```

Detailed implementation decisions, commands, troubleshooting, and validation results are maintained in the changelog notes.

---

# Architecture

## Core Data and ML Architecture

The original platform is built as a dependency-driven pipeline. Each stage produces data or artifacts required by later stages.

```text
Weather Data
     │
     ▼
W1  Collection & Cleaning
     │
     ▼
W2  ETL & Validation
     │
     ▼
W3  PostgreSQL
     │
     ▼
W4  Airflow Orchestration
     │
     ▼
W5  PySpark ETL
     │
     ▼
W6  Object Storage + Dashboard
     │
     ▼
W7  Feature Engineering
     │
     ▼
W8  Model Training & Evaluation
     │
     ▼
W9  Batch Prediction
     │
     ├──────────────► Prediction Artifacts
     │
     ▼
W10 FastAPI + Dashboard
     │
     ▼
W11 Deployment
```

### Component Responsibilities

| Component | Responsibility |
|---|---|
| Python | Application and pipeline implementation |
| Pandas | Data cleaning, transformation, feature engineering, and analysis |
| PostgreSQL | Structured relational weather-data storage |
| Airflow | Scheduling, dependency management, and execution of pipeline tasks |
| PySpark | Large-scale ETL and Spark SQL processing |
| MinIO | Local/self-hosted S3-compatible object storage |
| Amazon S3 | Cloud storage for pipeline artifacts |
| Scikit-learn | Model training, comparison, and evaluation |
| Joblib | Serialisation and loading of trained ML artifacts |
| FastAPI | REST API for prediction serving |
| Plotly Dash | Interactive prediction dashboard |
| Docker | Reproducible application packaging |
| Docker Compose | Local multi-service execution |
| Kubernetes/K3s | Container orchestration |
| Oracle Cloud | Cloud infrastructure hosting the K3s cluster |
| GitHub Actions | Automated validation, image building, publishing, and deployment |
| GHCR | Container image registry |

---

# Phase 1 — Data Engineering and Machine Learning

## W1 — Weather Data Collection and Cleaning

W1 establishes the source weather dataset and prepares it for downstream processing.

Main responsibilities:

- Download weather data
- Store raw data separately from processed data
- Clean the dataset
- Handle data-quality issues
- Apply project configuration
- Produce processed weather data

Implementation:

```text
w1_weather_data_cleaner/
├── data/
│   ├── raw/
│   └── processed/
└── src/
    ├── download.py
    ├── clean.py
    ├── config.py
    └── main.py
```

---

## W2 — Weather ETL Pipeline

W2 separates the ETL process into extraction, transformation, loading, and validation.

Main responsibilities:

- Extract weather data
- Transform and standardise records
- Validate the transformed dataset
- Load processed output
- Provide a reusable ETL entry point

Implementation:

```text
w2_weather_etl_pipeline/
└── src/
    ├── extract.py
    ├── transform.py
    ├── validate.py
    ├── load.py
    ├── config.py
    └── main.py
```

---

## W3 — PostgreSQL Data Loader

W3 introduces a relational database for structured weather data.

PostgreSQL provides:

- Persistent structured storage
- Database connectivity
- Data loading
- Load validation
- A database layer for downstream pipeline operations

Implementation:

```text
w3_postgresql_loader/
└── src/
    ├── database.py
    ├── load_data.py
    ├── validate_load.py
    ├── config.py
    └── main.py
```

---

## W4 — Airflow Weather Pipeline

W4 introduces Apache Airflow as the workflow orchestration layer.

Airflow manages:

- Task dependencies
- Pipeline execution order
- Scheduled execution
- Data extraction and transformation tasks
- Database operations
- Validation
- Pipeline cleanup

The W4 implementation contains reusable pipeline modules for extraction, transformation, loading, validation, database access, and cleanup.

Airflow is an orchestration system. It does not replace PostgreSQL, Spark, S3, or Kubernetes; it coordinates work performed by those components.

---

## W5 — PySpark ETL

W5 introduces Apache Spark for distributed data processing.

The project uses PySpark for:

- Weather-data ETL
- Spark DataFrame processing
- Spark SQL analysis
- Comparison with Pandas-based processing

The purpose of W5 is to demonstrate distributed processing capability and Spark-based data engineering rather than to replace every Pandas operation in the project.

Implementation:

```text
w5_spark_weather_etl/
├── notebooks/
│   └── spark_etl_analysis.ipynb
├── tests/
└── weather_etl/
    ├── extract.py
    ├── transform.py
    ├── load.py
    ├── spark_sql_analysis.py
    ├── config.py
    └── main.py
```

---

## W6 — Dashboard and Object Storage

W6 introduces object storage and the first dashboard layer.

### MinIO

MinIO provides an S3-compatible object-storage interface for local and self-hosted development.

The project uses it to store and retrieve weather data and artifacts through an object-storage workflow.

### Dashboard

Plotly Dash provides an interactive visualisation layer for weather data.

Implementation:

```text
w6_dashboard_minio/
└── src/
    ├── minio_client.py
    ├── upload_to_minio.py
    ├── data_loader.py
    ├── dashboard.py
    ├── app.py
    └── main.py
```

---

## W7 — Feature Engineering

W7 transforms processed weather data into machine-learning-ready features.

Feature engineering can include:

- Numerical feature preparation
- Time-based features
- Weather-variable transformations
- Feature selection/preparation
- Creation of the final feature dataset

The resulting dataset is stored as:

```text
w7_feature_engineering/data/processed/
```

The final feature dataset is the input to W8 model training and W9 prediction.

---

## W8 — Machine Learning Model

W8 trains and evaluates weather prediction models using Scikit-learn.

The project includes:

- Linear Regression
- Random Forest
- Model comparison
- Model evaluation
- Prediction generation
- Model serialisation
- Feature scaling where required
- Evaluation figures

Model artifacts include:

```text
w8_weather_prediction_model/models/
├── best_model.pkl
├── linear_regression_model.pkl
├── random_forest_model.pkl
├── scaler.pkl
└── model_metrics.json
```

### Model Training

The current validated model configuration uses Linear Regression as the selected production model.

The latest recorded model performance is:

| Metric | Result |
|---|---:|
| Model | Linear Regression |
| R² | 0.99 |
| RMSE | 0.52 °C |
| MAE | 0.37 °C |
| Engineered records | 43,488 |
| Training run | 27 Aug 2026 |

The model was selected based on evaluation rather than assuming that a more complex algorithm would automatically provide better predictions.

The repository also retains the Random Forest model and model-comparison outputs so that the selection process is reproducible.

---

## W9 — ML Prediction Pipeline

W9 separates prediction from model training.

The pipeline:

1. Loads the engineered feature dataset.
2. Loads the trained model.
3. Generates predictions.
4. Evaluates predictions against actual values.
5. Saves prediction results.
6. Uploads prediction artifacts to object storage.

### Batch Prediction

**Batch prediction** means running the trained model against a prepared collection of records and producing a set of predictions in one pipeline execution.

It is different from online prediction through FastAPI:

```text
Batch Prediction
Feature Dataset
      │
      ▼
Trained Model
      │
      ▼
Many Predictions
      │
      ▼
Prediction File
```

FastAPI instead handles prediction requests individually through an API.

---

## W10 — FastAPI and Prediction Dashboard

W10 provides the application layer.

### FastAPI

FastAPI exposes prediction functionality through HTTP endpoints.

The service includes:

- Model loading
- Prediction logic
- Request validation
- Response schemas
- API routes
- Application configuration

Implementation:

```text
w10_fastapi_service/app/
├── config.py
├── main.py
├── model_loader.py
├── predictor.py
├── routes.py
└── schemas.py
```

### Dashboard

The Plotly Dash application provides an interactive interface for prediction results.

It includes:

- API communication
- Prediction loading
- Live prediction loading
- Dashboard callbacks
- Layout
- Styling

Implementation:

```text
w10_fastapi_service/dashboard/
├── api_client.py
├── app.py
├── callbacks.py
├── layout.py
├── live_prediction_loader.py
├── prediction_loader.py
└── styles.py
```

---

## W11 — Initial Deployment Layer

The repository contains a deployment module for the original application deployment work.

```text
w11_deployment/
├── README.md
├── diagrams/
├── render/
└── screenshots/
```

The `render/` directory contains deployment configuration for the FastAPI and Dashboard applications.

Phase 2 subsequently moves the platform toward Kubernetes and Oracle Cloud as the main infrastructure architecture.

---

# Data and Artifact Storage

The project uses different storage technologies for different purposes.

| Storage | Purpose |
|---|---|
| Local filesystem | Development inputs, intermediate datasets, figures, and model files |
| PostgreSQL | Structured weather data |
| MinIO | Local/self-hosted S3-compatible object storage |
| Amazon S3 | Cloud storage for pipeline artifacts |
| Kubernetes PVC | Persistent storage for Kubernetes stateful services |

These technologies are complementary rather than interchangeable.

---

# AWS S3 Integration

Amazon S3 is used as the cloud object-storage layer for pipeline artifacts.

The project uses AWS through the orchestration layer and application deployment workflow.

## S3 Functions

The storage utilities in:

```text
orchestration/cloud_storage.py
```

provide the project's cloud-storage operations.

The workflow supports:

- Uploading generated artifacts to S3
- Downloading artifacts from S3
- Checking object availability
- Synchronising generated pipeline outputs
- Making fresh artifacts available to application workloads

Typical artifacts include:

```text
W7
└── w7_features_final.parquet

W8
├── best_model.pkl
├── scaler.pkl
└── model_metrics.json

W9
└── weather_predictions.csv
```

### Artifact Flow

```text
W7 Features
     │
     ▼
W8 Model Training
     │
     ├── Model
     ├── Scaler
     └── Metrics
     │
     ▼
W9 Batch Prediction
     │
     └── Predictions
     │
     ▼
Amazon S3
     │
     ▼
Application Artifact Refresh
     │
     ├── FastAPI
     └── Dashboard
```

The application workloads can retrieve the current artifacts from S3 rather than requiring the model and prediction files to be permanently embedded in the container image.

---

# Archive and Historical Data Handling

The orchestration layer includes archive checking and historical gap detection.

```text
orchestration/
├── check_archive.py
├── cloud_storage.py
├── config.py
├── create_db.py
└── test_cloud_storage.py
```

`check_archive.py` is responsible for identifying gaps in the historical weather archive so that missing periods can be detected before downstream processing.

This supports recovery and historical-data completeness rather than assuming that every expected weather record already exists.

---

# Phase 2 — Cloud-Native Platform

Phase 2 extends the Phase 1 pipeline into a deployable platform.

```text
Phase 1
Data + ML + Applications
          │
          ▼
P2-W1 Kubernetes Foundation
          │
          ▼
P2-W2 Platform Consolidation
          │
          ▼
P2-W3 Oracle Cloud / K3s
          │
          ▼
P2-W4 CI/CD
          │
          ▼
P2-W5 Public Deployment
          │
          ▼
P2-W6 MLflow + Optimisation
          │
          ▼
P2-W7 Comprehensive Testing
          │
          ▼
P2-W8 Monitoring + Final Integration
```

---

# P2-W1 — Kubernetes Foundation

P2-W1 establishes Kubernetes as the platform runtime.

The project uses:

- Kubernetes
- K3s
- kubectl
- Kubernetes Deployments
- StatefulSets
- Services
- PersistentVolumeClaims
- Secrets
- RBAC

### Stateful Services

PostgreSQL and MinIO are deployed as stateful workloads because their data must survive application Pod replacement.

### Airflow

Airflow is deployed using separate Kubernetes workloads for:

- Init
- API Server
- Scheduler
- DAG Processor

The custom project image contains the Airflow environment together with the project pipeline code.

---

# P2-W2 — Platform Consolidation

P2-W2 establishes the project root `Dockerfile` as the canonical image definition.

The unified image contains the dependencies and application code required across:

```text
Airflow
W1-W9
Spark
Machine Learning
FastAPI
Dashboard
```

The same image definition supports both:

- Docker Compose
- Kubernetes

This reduces environment drift between local development and deployment.

The phase also integrated W10 into the Airflow/Kubernetes lifecycle and reconstructed historical archive-gap detection.

---

# P2-W3 — Oracle Cloud and K3s

The consolidated platform is deployed to an Oracle Cloud ARM64 VM running K3s.

The cluster provides the runtime for:

```text
PostgreSQL
MinIO
Airflow
FastAPI
Dashboard
```

The deployment uses Kubernetes resource requests and limits so that workloads operate within the available cloud resources.

Persistent storage is maintained for PostgreSQL and MinIO through PVCs.

---

# Kubernetes Storage

Stateful storage is separated from replaceable application Pods.

```text
PostgreSQL Pod
      │
      ▼
PostgreSQL PVC
      │
      ▼
Persistent Volume


MinIO Pod
      │
      ▼
MinIO PVC
      │
      ▼
Persistent Volume
```

Deployments can therefore replace application Pods without intentionally deleting the persistent database and object-storage volumes.

Recovery validation is part of the Phase 2 testing strategy.

---

# Kubernetes Security and Configuration

The platform uses Kubernetes Secrets for sensitive runtime configuration.

The project uses a Kubernetes Secret named:

```text
weather-env
```

Secrets are referenced by workloads rather than storing their values in application manifests.

RBAC is also configured for Airflow-related Kubernetes access.

The repository should contain configuration references, not secret values or private credentials.

---

# P2-W4 — CI/CD

P2-W4 connects Git-based development with automated deployment.

```text
Code Change
    │
    ▼
GitHub
    │
    ▼
GitHub Actions
    │
    ├── Validate repository
    ├── Run tests
    ├── Build image
    └── Publish image
            │
            ▼
           GHCR
            │
            ▼
      Oracle K3s
            │
            ▼
   Kubernetes Rollout
```

## CI

The CI workflow validates the project before an image is published.

It includes:

- Git-based workflow triggers
- Repository validation
- Python environment setup
- Automated tests
- Docker image build validation

Deployable changes include relevant application, orchestration, dependency, Docker, Kubernetes, DAG, and test changes.

Documentation-only changes do not need to trigger an application deployment.

## Container Registry

GitHub Container Registry stores the built project images.

Images use the Git commit SHA as their version identifier:

```text
<image>:<commit-sha>
```

This provides a traceable relationship between:

```text
Git Commit
    ↕
Container Image
    ↕
Kubernetes Deployment
```

The CI build produces:

```text
linux/amd64
linux/arm64
```

The ARM64 image is required for the Oracle Cloud ARM64 environment.

## Deployment

GitHub Actions can deploy the selected image to the Oracle K3s cluster and perform the Kubernetes rollout.

The deployment uses Kubernetes configuration already maintained in:

```text
k8/
```

Persistent database and object-storage PVCs are not deleted as part of the normal application rollout.

## Rollback

Versioned images provide the basis for rollback.

The rollback model is:

```text
Working Version
      │
      ▼
New Version
      │
      ▼
Problem Detected
      │
      ▼
Restore Previous Image
      │
      ▼
Kubernetes Rollout
      │
      ▼
Recovered Application
```

Rollback and recovery validation completes the CI/CD lifecycle.

---

# Kubernetes Repository

The Kubernetes configuration is organised by platform component:

```text
k8/
├── airflow/
├── dashboard/
├── fastapi/
├── minio/
└── postgres/
```

The manifests define the Kubernetes resources required to deploy the platform.

Supporting deployment documentation and command references are maintained separately.

---

# Technology Stack

## Data Engineering

- Python
- Pandas
- PySpark
- Spark SQL
- PostgreSQL
- Apache Airflow

## Storage

- Local filesystem
- PostgreSQL
- MinIO
- Amazon S3
- Boto3
- AWS CLI
- Kubernetes PersistentVolumes/PVCs

## Machine Learning

- Scikit-learn
- Linear Regression
- Random Forest
- Joblib
- PyArrow

## Application

- FastAPI
- Uvicorn
- Plotly Dash

## Containerisation

- Docker
- Docker Compose
- Docker Buildx
- QEMU
- Multi-platform images

## Kubernetes and Cloud

- Kubernetes
- K3s
- kubectl
- Kubernetes Secrets
- Kubernetes RBAC
- Oracle Cloud

## CI/CD

- Git
- GitHub
- GitHub Actions
- GitHub Container Registry

---

# Repository Structure

The complete repository structure is maintained directly in the GitHub repository.

See the repository root for the current folders, modules, Kubernetes manifests, configuration, tests, and documentation.

# Development and Deployment Workflow

The normal development path is:

```text
VS Code
   │
   ▼
Local Validation
   │
   ▼
GitHub Desktop
   │
   ▼
GitHub
   │
   ▼
GitHub Actions
   │
   ▼
Container Image
   │
   ▼
GHCR
   │
   ▼
Oracle K3s
```

GitHub Actions provides the automated bridge between source-code changes and the deployed Kubernetes platform.

---

# Current Project Status

## Phase 1

| Stage | Status |
|---|---|
| W1 Data Collection & Cleaning | Complete |
| W2 ETL Pipeline | Complete |
| W3 PostgreSQL Loader | Complete |
| W4 Airflow Orchestration | Complete |
| W5 PySpark ETL | Complete |
| W6 Dashboard + Object Storage | Complete |
| W7 Feature Engineering | Complete |
| W8 Model Training & Evaluation | Complete |
| W9 Batch Prediction | Complete |
| W10 FastAPI + Dashboard | Complete |
| W11 Initial Deployment Layer | Implemented |

## Phase 2

| Stage | Status |
|---|---|
| P2-W1 Kubernetes Foundation + W1-W9 Migration | Complete |
| P2-W2 Platform Consolidation + W10 Integration | Complete |
| P2-W3 Oracle Cloud / K3s Deployment | Complete |
| P2-W4 CI/CD | In Progress |
| P2-W5 Public Deployment | Planned |
| P2-W6 MLflow + Platform Optimisation | Planned |
| P2-W7 Comprehensive Testing | Planned |
| P2-W8 Monitoring + Final Integration | Planned |

---

# Project Objective

The project demonstrates how a data engineering and machine learning workflow can evolve into a deployable platform.

```text
Data
 │
 ▼
Engineering
 │
 ▼
Storage
 │
 ▼
Orchestration
 │
 ▼
Distributed Processing
 │
 ▼
Feature Engineering
 │
 ▼
Machine Learning
 │
 ▼
Prediction
 │
 ▼
API + Dashboard
 │
 ▼
Containers
 │
 ▼
Kubernetes
 │
 ▼
Cloud
 │
 ▼
CI/CD
```

The emphasis is on integrating the technologies into one reproducible system rather than building unrelated technology demonstrations.

---

# Documentation

The README provides the architecture and purpose of the platform.

Detailed implementation information is maintained in the project documentation, including:

- Weekly development work
- Phase 2 daily changelog notes
- Exact commands used
- Configuration changes
- Kubernetes deployment work
- CI/CD implementation
- Troubleshooting
- Validation results
- Implementation decisions

The `changelog_notes/` directory is the detailed development record; the README intentionally remains a concise technical overview.
