# Weather Intelligence Platform

An end-to-end data engineering and machine learning platform for processing weather data, orchestrating the complete data pipeline, generating ML-ready features, training prediction models, serving predictions through FastAPI, and presenting results through an interactive Dashboard.

The project began as a 12-week data engineering and ML build and has been extended into a cloud-native platform using Docker, Kubernetes, Oracle Cloud, GitHub Actions, and GitHub Container Registry.

---

## Overview

The platform covers the complete data and machine learning lifecycle:

- Weather data collection and cleaning
- ETL processing
- PostgreSQL data storage
- Apache Airflow workflow orchestration
- PySpark data processing
- MinIO / S3-compatible object storage
- Feature engineering (transforming weather data into ML-ready features)
- Machine learning model training and evaluation
- Batch prediction
- FastAPI prediction service
- Interactive weather prediction Dashboard
- Docker containerisation
- Kubernetes deployment
- Oracle Cloud K3s deployment
- GitHub Actions CI/CD
- GitHub Container Registry (GHCR)
- Immutable commit-SHA container images
- Automated deployment from GitHub to Oracle K3s
- Persistent storage for PostgreSQL and MinIO

The platform is designed around the following development and deployment workflow:

```text
Local Change
     ↓
Local Testing
     ↓
GitHub Desktop
     ↓
GitHub
     ↓
GitHub Actions
     ↓
Validation + Tests
     ↓
Multi-platform Docker Build
     ↓
GitHub Container Registry
     ↓
Oracle Cloud K3s
     ↓
Kubernetes Rollout
     ↓
Updated Platform
```

---

# Architecture

## Data Engineering and ML Pipeline

Apache Airflow is the central orchestration layer for the W1-W10 pipeline. It coordinates the processing stages and the movement of data and artifacts between the processing, database, object-storage, machine-learning, and application components.

PostgreSQL and MinIO are infrastructure services used by the pipeline. They are deployed and managed as Kubernetes workloads, while Airflow orchestrates the pipeline tasks that use those services.

```text
                         WEATHER DATA
                              │
                              ▼
                 ┌────────────────────────┐
                 │ W1 — Data Collection & │
                 │      Cleaning          │
                 └───────────┬────────────┘
                             ▼
                 ┌────────────────────────┐
                 │ W2 — ETL Pipeline      │
                 └───────────┬────────────┘
                             ▼
                 ┌────────────────────────┐
                 │ W3 — PostgreSQL Loader │
                 └───────────┬────────────┘
                             ▼
                 ┌────────────────────────┐
                 │ W4 — Airflow           │
                 │      Orchestration     │
                 └───────────┬────────────┘
                             ▼
                 ┌────────────────────────┐
                 │ W5 — PySpark ETL       │
                 └───────────┬────────────┘
                             ▼
                 ┌────────────────────────┐
                 │ W6 — MinIO / S3        │
                 │      + Dashboard Data  │
                 └───────────┬────────────┘
                             ▼
                 ┌────────────────────────┐
                 │ W7 — Feature           │
                 │      Engineering       │
                 │ (ML-ready features)    │
                 └───────────┬────────────┘
                             ▼
                 ┌────────────────────────┐
                 │ W8 — ML Model Training │
                 └───────────┬────────────┘
                             ▼
                 ┌────────────────────────┐
                 │ W9 — Batch Prediction  │
                 └───────────┬────────────┘
                             ▼
                 ┌────────────────────────┐
                 │ W10 — FastAPI +        │
                 │       Dashboard        │
                 └────────────────────────┘
```

### Airflow's Role

Airflow is not only responsible for the FastAPI and Dashboard layer.

It acts as the **central workflow orchestrator** for the full W1-W10 processing pipeline.

In simple terms:

```text
Airflow
  │
  ├── Coordinates data ingestion and cleaning
  ├── Coordinates ETL processing
  ├── Coordinates PostgreSQL loading
  ├── Coordinates PySpark processing
  ├── Coordinates object-storage operations
  ├── Coordinates feature engineering
  ├── Coordinates ML processing
  ├── Coordinates batch prediction
  └── Produces / prepares outputs consumed by
      FastAPI and the Dashboard
```

PostgreSQL and MinIO themselves run as persistent Kubernetes services. Airflow coordinates the pipeline tasks that create, process, load, read, and publish the required data and artifacts.

---

# Production / Cloud Architecture

Phase 2 adds a production engineering layer around the original W1-W10 platform.

```text
                    LOCAL DEVELOPMENT
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
              ┌────────────┼────────────┐
              ▼            ▼            ▼
           Changes       Tests       Docker Build
           Detection    + Validation
              │            │            │
              └────────────┼────────────┘
                           ▼
                 Multi-platform Image
                    AMD64 + ARM64
                           │
                           ▼
                          GHCR
                           │
                           ▼
                  Oracle Cloud VM
                           │
                           ▼
                          K3s
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   PostgreSQL            MinIO             Airflow
   Data Store          Object Store       Orchestrator
        │                  │                  │
        │                  │          ┌───────┴───────┐
        │                  │          ▼               ▼
        │                  │       FastAPI        Dashboard
        │                  │
        └──────────────────┴──────────────────────────┐
                                                       │
                                                       ▼
                                           W1-W10 Pipeline
                                           Orchestrated by
                                               Airflow
```


### AWS S3 in the Production Data Flow

The cloud deployment uses AWS S3 as the cloud-backed artifact layer between the Airflow-orchestrated data/ML pipeline and the application services.

```text
                    Oracle Cloud / K3s
                           │
                           ▼
                      Apache Airflow
                           │
                    W1-W10 Pipeline
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
        PostgreSQL                  AWS S3
        structured data            cloud artifacts
                                         │
                                         ├── W7 features
                                         ├── W8 model
                                         ├── scaler
                                         ├── metrics
                                         └── W9 predictions
                                         │
                                         ▼
                              FastAPI / Dashboard
```

This creates a clear separation of responsibilities:

- **PostgreSQL** — structured relational data storage.
- **MinIO** — Kubernetes-hosted S3-compatible object storage used as part of the platform infrastructure.
- **AWS S3** — cloud-backed storage for the current data/ML/application artifacts used by the deployed workflow.
- **Apache Airflow** — orchestration layer responsible for coordinating processing and artifact publication.
- **FastAPI / Dashboard** — application layer consuming the current artifacts from S3.

The AWS S3 integration is also retained as the storage foundation for the planned P2-W6 model artifact tracking and lifecycle-management work.

### Infrastructure vs Orchestration

The production architecture has two related but different responsibilities:

**Kubernetes / K3s**

- Runs PostgreSQL
- Runs MinIO
- Runs Airflow
- Runs FastAPI
- Runs Dashboard
- Manages Pods, Services, Deployments and StatefulSets
- Provides persistent volumes for PostgreSQL and MinIO

**Apache Airflow**

- Orchestrates the W1-W10 data and ML workflow
- Coordinates pipeline tasks
- Coordinates processing dependencies and execution order
- Uses PostgreSQL and MinIO as platform services
- Coordinates outputs that are eventually consumed by FastAPI and the Dashboard

**GitHub Actions**

- Validates changes
- Runs tests
- Builds the unified Docker image
- Publishes the image to GHCR
- Deploys updated workloads to Oracle K3s

---

# Project Modules

| Stage | Module | Description | Main Technology |
|---|---|---|---|
| W1 | Data Collection & Cleaning | Collect and clean historical weather data | Python / Pandas |
| W2 | ETL Pipeline | Transform and prepare weather data for downstream processing | Python / Pandas |
| W3 | PostgreSQL Loader | Load structured weather data into PostgreSQL | PostgreSQL / Python |
| W4 | Airflow Orchestration | Orchestrate the complete W1-W10 pipeline | Apache Airflow |
| W5 | Spark ETL | Process weather data using distributed processing | PySpark |
| W6 | Data Lake + Dashboard | Store data/artifacts and provide visualisation | MinIO / S3 / Plotly Dash |
| W7 | Feature Engineering | Transform weather data into ML-ready features | Pandas / PyArrow |
| W8 | Machine Learning Model | Train and evaluate the prediction model | Scikit-learn |
| W9 | Batch Prediction | Generate predictions from the trained model | Python / Joblib |
| W10 | FastAPI + Dashboard | Serve predictions and integrate the Dashboard | FastAPI / Plotly Dash |
| P2-W1 | Kubernetes Foundation | Migrate the platform to Kubernetes | Kubernetes / K3s |
| P2-W2 | Platform Consolidation | Consolidate W1-W10 into one deployable image | Docker / Kubernetes |
| P2-W3 | Cloud Deployment | Deploy the platform to Oracle Cloud K3s | Oracle Cloud / K3s |
| P2-W4 | CI/CD | Automate validation, image publishing and deployment | GitHub Actions / GHCR |

---


Airflow is the control plane for this data/artifact movement. The application layer retrieves the latest S3 artifacts after the pipeline refreshes the deployed services.

# W1-W10 Data Flow

```text
W1
│
├── Historical weather data
│
▼
W2
│
├── Cleaned / transformed data
│
▼
W3
│
├── PostgreSQL
│
▼
W4
│
├── Airflow orchestration
│
▼
W5
│
├── PySpark processing
│
▼
W6
│
├── MinIO / S3-compatible storage
├── Dashboard data
│
▼
W7
│
├── Feature engineering
├── ML-ready feature dataset
│
▼
W8
│
├── Model training
├── Model evaluation
│
▼
W9
│
├── Batch predictions
│
▼
W10
│
├── FastAPI prediction service
└── Interactive Dashboard
```

---

# Machine Learning Pipeline

Feature engineering means transforming the processed weather data into useful input variables that can be consumed by the machine-learning model.

```text
Weather Data
     │
     ▼
W7 — Feature Engineering
     │
     │ Transform weather data
     │ into ML-ready features
     ▼
Feature Dataset
     │
     ▼
W8 — Model Training
     │
     ▼
Trained ML Model
     │
     ▼
W9 — Batch Prediction
     │
     ▼
Prediction Results
     │
     ▼
W10 — FastAPI
     │
     ▼
Dashboard
```

The trained model and prediction artifacts are integrated into the application layer so that predictions can be accessed through FastAPI and presented through the Dashboard.

---

# Technology Stack

## Data Engineering

- Python
- Pandas
- PostgreSQL
- PySpark
- Apache Airflow

## Storage

- PostgreSQL
- MinIO
- Amazon S3 (AWS S3)
- Kubernetes Persistent Volumes

### AWS

- Amazon S3
- AWS region: `eu-west-2`
- Bucket: `weather-data-lake-mlops`


### AWS S3 Cloud Data and Artifact Layer

AWS S3 is an active cloud object-storage layer in the deployed W1-W10 data and machine-learning workflow. It is used by the orchestration layer to persist processed datasets and ML/application artifacts that are consumed by downstream services.

The project uses:

```text
AWS S3 Bucket: weather-data-lake-mlops
AWS Region: eu-west-2
```

The validated artifact flow is:

```text
W1-W10 Pipeline
      │
      ▼
Apache Airflow
      │
      ▼
AWS S3
      ├── features/w7_features_final.parquet
      ├── models/best_model.pkl
      ├── models/scaler.pkl
      ├── models/model_metrics.json
      └── predictions/weather_predictions.csv
      │
      ▼
FastAPI / Dashboard
```

The orchestration package contains the cloud-storage integration used for S3 operations:

```text
orchestration/
├── cloud_storage.py
└── test_cloud_storage.py
```

Airflow coordinates the W1-W10 processing lifecycle and uploads the resulting feature, model, prediction, and metrics artifacts to S3. The deployed FastAPI and Dashboard workloads then retrieve the current artifacts from S3.

For Kubernetes deployment, the FastAPI and Dashboard workloads use AWS CLI-based init containers together with the `weather-env` Kubernetes Secret to download the required S3 artifacts before the application starts.

When a new pipeline execution produces updated artifacts, the Airflow lifecycle refreshes the application Pods. The replacement Pods download the latest S3 artifacts, preventing the application layer from continuing to use stale feature, model, prediction, or metrics files.

This establishes the deployed data/artifact lifecycle as:

```text
Airflow
   ↓
W1-W10 Pipeline
   ↓
AWS S3
   ↓
Application Refresh
   ↓
FastAPI / Dashboard Pods replaced
   ↓
Latest S3 artifacts downloaded
   ↓
Updated prediction application
```

AWS S3 is therefore part of the production cloud architecture rather than a separate storage experiment.

## Machine Learning

- Scikit-learn
- Joblib
- PyArrow

## Application

- FastAPI
- Plotly Dash
- Uvicorn

## Infrastructure

- Docker
- Docker Compose
- Kubernetes
- K3s
- Oracle Cloud
- AWS S3
- Persistent Volumes / PVCs

## CI/CD

- GitHub
- GitHub Actions
- GitHub Container Registry (GHCR)
- Docker Buildx
- QEMU
- Multi-platform Docker images

---

# Phase 2 — Production Engineering

Phase 2 extends the original data engineering project into a cloud-native platform.

| Phase | Focus | Status |
|---|---|---|
| P2-W1 | Kubernetes Foundation + Airflow/W1-W9 Migration | Complete |
| P2-W2 | Platform Consolidation + W10 Integration | Complete |
| P2-W3 | Cloud / K3s Deployment | Complete |
| P2-W4 | CI/CD | In Progress |
| P2-W5 | Public Deployment | Planned |
| P2-W6 | MLflow + Platform Optimisation | Planned |
| P2-W7 | Comprehensive Testing | Planned |
| P2-W8 | Monitoring + Final Integration | Planned |

---

# P2-W1 — Kubernetes Foundation

The first Phase 2 stage established the Kubernetes foundation and migrated the existing platform components.

Key areas included:

- Kubernetes / K3s foundation
- Kubernetes node readiness
- PostgreSQL StatefulSet
- PostgreSQL PersistentVolumeClaim
- PostgreSQL Service
- MinIO StatefulSet
- MinIO PersistentVolumeClaim
- MinIO Service
- Airflow platform migration
- W1-W9 integration
- Kubernetes Secrets
- End-to-end platform validation

---

# P2-W2 — Platform Consolidation

The platform was consolidated around a single canonical project Dockerfile.

The unified image contains the dependencies and W1-W10 application code required by:

- Airflow
- W1-W9 processing
- Spark
- Machine learning
- FastAPI
- Dashboard

The same canonical image can therefore be used across the Docker and Kubernetes environments.

---

# P2-W3 — Oracle Cloud / K3s

The consolidated platform was deployed to an Oracle Cloud ARM64 VM running K3s.

Current Kubernetes workloads include:

```text
PostgreSQL
MinIO
Airflow API Server
Airflow Scheduler
Airflow DAG Processor
Airflow Init Job
FastAPI
Prediction Dashboard
```

Persistent storage is configured for PostgreSQL and MinIO.

Kubernetes resource requests and limits are used to manage workloads within the available cloud VM resources.

---

# P2-W4 — CI/CD

The CI/CD pipeline automates the path from a local project change to the Oracle K3s deployment.

## CI/CD Flow

```text
Local Code Change
        │
        ▼
GitHub Desktop
        │
        ▼
Push to main
        │
        ▼
GitHub Actions
        │
        ├── Detect deployable changes
        ├── Set up Python
        ├── Validate repository structure
        ├── Run automated tests
        ├── Build Docker image
        └── Build AMD64 + ARM64 image
                    │
                    ▼
                   GHCR
                    │
                    ▼
             Oracle Cloud / K3s
                    │
                    ├── PostgreSQL
                    ├── MinIO
                    ├── Airflow
                    ├── FastAPI
                    └── Dashboard
```

## Deployable Change Detection

The workflow detects changes in project areas that require deployment, including:

- Dockerfile
- Dependency files
- Docker Compose files
- Kubernetes manifests
- Airflow DAGs
- Orchestration code
- Tests
- W1-W10 application code

Documentation-only changes can therefore avoid an unnecessary application image build and deployment.

## Container Images

Images are published to GitHub Container Registry using the Git commit SHA:

```text
ghcr.io/gaurav-dwivedi-de/data_engineering_portfolio:<commit-sha>
```

Using the commit SHA provides an identifiable version for each deployment instead of relying on a mutable `latest` tag.

The CI pipeline builds:

```text
linux/amd64
linux/arm64
```

This supports the GitHub Actions build environment and the ARM64 Oracle Cloud environment.

## Automated Deployment

The Oracle deployment synchronises the project repository from GitHub and applies the Kubernetes configuration.

Deployment order:

```text
1. PostgreSQL
2. MinIO
3. Airflow Init
4. Airflow
5. FastAPI
6. Dashboard
```

FastAPI and Dashboard Services are also applied automatically.

Normal deployments use Kubernetes `apply` operations and do not delete PostgreSQL or MinIO PersistentVolumeClaims.

---

# Persistent Storage

PostgreSQL and MinIO use Kubernetes PersistentVolumeClaims.

```text
PostgreSQL
    │
    ▼
postgres-data PVC
    │
    ▼
Persistent Storage


MinIO
    │
    ▼
minio-data PVC
    │
    ▼
Persistent Storage
```

Application Pods may be replaced during a deployment while the persistent volumes remain in place.

The normal CI/CD workflow does not delete these PVCs.

---

# Secrets and Configuration

Sensitive configuration is kept outside the public source repository.

Kubernetes workloads reference the Kubernetes Secret:

```text
weather-env
```

The repository contains references to the Secret but not the actual secret values.

Sensitive values such as database credentials, object-storage credentials, cloud credentials, and SSH private keys should never be committed to GitHub.

---

# Testing

The CI pipeline currently contains an initial automated test layer and repository validation.

Current test location:

```text
tests/
└── test_project_imports.py
```

The initial tests validate core Python and machine-learning dependencies.

CI also validates the expected repository structure and verifies that the unified Docker image can be built successfully.

Testing will be expanded during P2-W7 to cover:

- W1-W10 components
- Data-quality behaviour
- Archive and recovery logic
- PostgreSQL
- MinIO / S3
- Airflow
- Kubernetes
- FastAPI
- Dashboard
- Complete W1-W10 end-to-end execution

---

# Repository Structure

```text
data_engineering_portfolio/
│
├── dags/
├── orchestration/
├── tests/
│
├── k8/
│   ├── airflow/
│   ├── dashboard/
│   ├── fastapi/
│   ├── minio/
│   └── postgres/
│
├── w1_weather_data_cleaner/
├── w2_weather_etl_pipeline/
├── w3_postgresql_loader/
├── w4_airflow_weather_pipeline/
├── w5_spark_weather_etl/
├── w6_dashboard_minio/
├── w7_feature_engineering/
├── w8_weather_prediction_model/
├── w9_ml_pipeline/
├── w10_fastapi_service/
│
├── Dockerfile
├── docker-compose.yml
├── docker-compose.resolved.yml
├── docker_requirements.txt
└── README.md
```

Detailed implementation history is maintained separately in the project changelog documentation.

---

# Development Workflow

Normal local Git operations use GitHub Desktop:

```text
VS Code
   │
   ▼
Local Testing
   │
   ▼
GitHub Desktop
   │
   ├── Review changes
   ├── Commit
   └── Push
   │
   ▼
GitHub
   │
   ▼
GitHub Actions
   │
   ▼
Automated CI/CD
```

GitHub Actions performs automated validation, image publishing and deployment after a qualifying push.

---

# Current Project Status

## Completed

### Original W1-W10 Platform

- W1 Data Collection and Cleaning
- W2 ETL Pipeline
- W3 PostgreSQL Loader
- W4 Airflow Orchestration
- W5 PySpark ETL
- W6 MinIO / S3 Data Lake + Dashboard
- W7 Feature Engineering
- W8 Machine Learning Model
- W9 Batch Prediction
- W10 FastAPI + Dashboard Integration

### Phase 2

- P2-W1 Kubernetes Foundation + W1-W9 Migration
- P2-W2 Platform Consolidation + W10 Integration
- P2-W3 Oracle Cloud / K3s Deployment
- PostgreSQL Kubernetes deployment
- MinIO Kubernetes deployment
- Airflow Kubernetes deployment
- FastAPI Kubernetes deployment
- Dashboard Kubernetes deployment
- Persistent storage configuration
- GitHub Actions CI
- Automated project validation
- Initial automated tests
- Unified Docker image build
- GHCR integration
- Immutable commit-SHA image tagging
- Multi-platform AMD64 / ARM64 image builds
- Automated Oracle K3s deployment
- FastAPI Kubernetes Service deployment
- Dashboard Kubernetes Service deployment

---

# Current Milestone

## P2-W4 — CI/CD

The main CI/CD workflow is operational:

```text
Local change
    ↓
GitHub Desktop
    ↓
GitHub
    ↓
GitHub Actions
    ↓
Tests + Validation
    ↓
Docker Image
    ↓
GHCR
    ↓
Oracle Cloud K3s
    ↓
Kubernetes Rollout
```

A real application change has been used to verify the automated GitHub-to-Oracle deployment path.

Airflow has also been verified on Oracle, including successful execution of the weather pipeline.

The remaining P2-W4 work is rollback and recovery validation using versioned container images.

---

# Upcoming Work

## P2-W4 D5 — Rollback / Recovery

- Deploy a known working image version
- Deploy a newer version
- Validate Kubernetes rollout
- Demonstrate rollback to the previous image version
- Verify application recovery

## P2-W5 — Public Deployment

Planned work:

- Project domain and DNS
- Kubernetes ingress
- HTTPS / TLS
- Public FastAPI access
- Public Dashboard access
- Secure service routing
- Cloudflare integration

## P2-W6 — MLflow + Platform Optimisation

Planned work:

- MLflow integration with W8/W9
- Experiment tracking (recording model runs, parameters and metrics)
- Model artifact tracking
- Model versioning and lifecycle management
- Review of Spark, ML, Kubernetes, image, storage and dependency efficiency

## P2-W7 — Comprehensive Testing

Planned work:

- W1-W10 component testing
- Data-quality testing
- Archive and recovery testing
- PostgreSQL / MinIO / S3 testing
- Airflow and Kubernetes integration testing
- FastAPI / Dashboard testing
- Complete production-style W1-W10 end-to-end testing

## P2-W8 — Monitoring + Final Integration

Planned work:

- Airflow and pipeline monitoring
- Kubernetes workload monitoring
- PostgreSQL and MinIO monitoring
- FastAPI and Dashboard availability monitoring
- Final W1-W10 execution
- Data and artifact lineage verification
- Final architecture and deployment documentation
- Portfolio presentation and project cleanup

---

# Project Objective

The project demonstrates the complete lifecycle of a data engineering and machine learning platform:

```text
Data Ingestion
      ↓
Data Cleaning
      ↓
ETL
      ↓
Database
      ↓
Workflow Orchestration
      ↓
Distributed Processing
      ↓
Object Storage
      ↓
Feature Engineering
      ↓
Machine Learning
      ↓
Prediction API
      ↓
Dashboard
      ↓
Containerisation
      ↓
Kubernetes
      ↓
Cloud Deployment
      ↓
CI/CD
      ↓
Public Deployment
      ↓
Testing + Monitoring
```

The objective is to integrate these technologies into one reproducible platform rather than treating each component as an isolated exercise.

---

# Documentation

Detailed implementation history is maintained separately from this README.

The repository includes:

- Weekly project documentation
- Phase 2 daily development notes
- Kubernetes deployment documentation
- CI/CD development notes
- Infrastructure configuration
- Troubleshooting and implementation decisions

See the `changelog_notes/` directory for the chronological development history.
