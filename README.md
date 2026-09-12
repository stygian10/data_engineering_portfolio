# Weather Intelligence Platform

An end-to-end **data engineering, machine learning, and cloud deployment platform** for collecting weather data, cleaning and transforming it, loading it into PostgreSQL, orchestrating the workflow with Apache Airflow, processing data with PySpark, generating ML-ready features, training and evaluating prediction models, producing batch predictions, serving predictions through FastAPI, and presenting results through an interactive Plotly Dash dashboard.

The project began as a **Phase 1 data engineering and machine learning portfolio project** and was subsequently extended through **Phase 2** into a containerised, Kubernetes-based cloud platform running on Oracle Cloud K3s with GitHub Actions CI/CD and AWS S3-backed ML/data artifacts.

> **Current position:** Phase 1 W1-W10 is complete. Phase 2 P2-W1, P2-W2, and P2-W3 are complete. P2-W4 CI/CD D1-D4 are complete; the remaining P2-W4 rollback/recovery validation is the current milestone.

---

## Table of Contents

- [Project Overview](#project-overview)
- [What the Project Demonstrates](#what-the-project-demonstrates)
- [Phase 1 — Core Data Engineering and ML Platform](#phase-1--core-data-engineering-and-ml-platform)
- [W1-W10 Pipeline](#w1-w10-pipeline)
- [AWS S3 Artifact Architecture](#aws-s3-artifact-architecture)
- [Machine Learning](#machine-learning)
- [Phase 2 — Cloud-Native Platform Engineering](#phase-2--cloud-native-platform-engineering)
- [Kubernetes and Oracle Cloud](#kubernetes-and-oracle-cloud)
- [Docker and Platform Consolidation](#docker-and-platform-consolidation)
- [CI/CD](#cicd)
- [Storage and Persistence](#storage-and-persistence)
- [Secrets and Configuration](#secrets-and-configuration)
- [Testing and Validation](#testing-and-validation)
- [Technology Stack](#technology-stack)
- [Repository Structure](#repository-structure)
- [Development and Deployment Workflow](#development-and-deployment-workflow)
- [Current Status](#current-status)
- [Roadmap](#roadmap)
- [Documentation](#documentation)
- [Project Objective](#project-objective)

---

# Project Overview

The Weather Intelligence Platform integrates a complete data-to-application workflow rather than treating data engineering, machine learning, APIs, and infrastructure as separate exercises.

The platform currently combines:

- Historical weather data collection
- Data cleaning and validation
- Python/Pandas ETL
- PostgreSQL storage
- Apache Airflow orchestration
- PySpark ETL and Spark SQL analysis
- MinIO S3-compatible object storage
- AWS S3 cloud object storage
- Feature engineering
- Scikit-learn model training and evaluation
- Model artifact persistence
- Batch prediction
- FastAPI prediction serving
- Plotly Dash visualisation
- Docker and Docker Compose
- Kubernetes and K3s
- Kubernetes StatefulSets, Deployments, Services, PVCs and RBAC
- Oracle Cloud ARM64 deployment
- Kubernetes resource requests and limits
- Kubernetes Secrets
- GitHub Actions CI/CD
- GitHub Container Registry (GHCR)
- Immutable Git commit-SHA image versioning
- Multi-platform AMD64/ARM64 image builds
- Automated deployment from GitHub Actions to Oracle K3s
- S3-based model/data artifact refresh
- Application refresh after new pipeline artifacts are generated
- Archive-gap detection and recovery logic

The result is a portfolio project that demonstrates the progression:

**data engineering → ML pipeline → application layer → containerisation → Kubernetes → cloud deployment → CI/CD.**

---

# What the Project Demonstrates

From a portfolio perspective, the project demonstrates practical experience across several layers.

| Area | Demonstrated Capability |
|---|---|
| Data ingestion | Weather data collection and preparation |
| ETL | Extraction, transformation, validation and loading |
| Data quality | Validation and historical archive-gap detection |
| Relational storage | PostgreSQL |
| Workflow orchestration | Apache Airflow |
| Distributed processing | PySpark / Spark SQL |
| Object storage | MinIO and AWS S3 |
| Feature engineering | ML-ready feature generation |
| Machine learning | Scikit-learn regression model training/evaluation |
| Batch inference | Offline generation of predictions from a feature dataset |
| API serving | FastAPI |
| Visualisation | Plotly Dash |
| Packaging | Docker |
| Local orchestration | Docker Compose |
| Container orchestration | Kubernetes / K3s |
| Cloud | Oracle Cloud |
| Persistent storage | Kubernetes PVCs / StatefulSets |
| Secrets | Kubernetes Secret-based configuration |
| CI | GitHub Actions |
| Container registry | GHCR |
| Image versioning | Git commit-SHA tags |
| Multi-architecture builds | Linux AMD64 + ARM64 |
| Continuous deployment | GitHub Actions → Oracle K3s |
| Recovery design | Versioned-image rollback planned/validated in P2-W4 D5 |
| MLOps | MLflow planned for P2-W6 |

---

# Phase 1 — Core Data Engineering and ML Platform

Phase 1 established the original W1-W10 platform.

The major stages were:

| Stage | Component | Purpose | Primary Technology |
|---|---|---|---|
| W1 | Weather Data Cleaner | Collect, clean and prepare weather data | Python, Pandas |
| W2 | Weather ETL Pipeline | Extract, transform, validate and load processed data | Python, Pandas |
| W3 | PostgreSQL Loader | Persist structured weather data | PostgreSQL, Python |
| W4 | Airflow Weather Pipeline | Orchestrate the data pipeline | Apache Airflow |
| W5 | Spark Weather ETL | Process weather data with distributed processing | PySpark, Spark SQL |
| W6 | Dashboard + MinIO | Store and visualise processed weather data | MinIO, Plotly Dash |
| W7 | Feature Engineering | Create ML-ready features | Pandas, PyArrow |
| W8 | Weather Prediction Model | Train, compare and evaluate regression models | Scikit-learn |
| W9 | ML Pipeline | Load the model/features and generate predictions | Python, Joblib |
| W10 | FastAPI + Dashboard | Serve predictions and present results | FastAPI, Plotly Dash |

The repository also contains `w11_deployment/`, representing the earlier deployment work associated with the original project lifecycle. Phase 2 subsequently became the active, dependency-driven production/cloud deployment track.

---

# W1-W10 Pipeline

Apache Airflow became the central orchestration layer for the W1-W10 workflow.

Airflow coordinates the execution order and dependencies between data ingestion, transformation, database operations, Spark processing, feature engineering, model processing, prediction generation, artifact publication, and application refresh.

The important distinction is:

- **Airflow orchestrates the workflow.**
- **Kubernetes runs the platform workloads.**
- **PostgreSQL stores relational data.**
- **AWS S3 stores cloud data/ML artifacts.**
- **MinIO provides S3-compatible object storage used by the earlier/local platform and remains part of the Kubernetes infrastructure.**
- **FastAPI serves application predictions.**
- **Dash provides the interactive presentation layer.**

## Core pipeline

```text
Weather Data
     ↓
W1 — Collection + Cleaning
     ↓
W2 — ETL + Validation
     ↓
W3 — PostgreSQL
     ↓
W4 — Airflow Orchestration
     ↓
W5 — PySpark ETL / Spark SQL
     ↓
W6 — Object Storage + Dashboard Data
     ↓
W7 — Feature Engineering
     ↓
W8 — Model Training + Evaluation
     ↓
W9 — Batch Prediction
     ↓
W10 — FastAPI + Plotly Dash
```

This is the primary data/ML flow; additional infrastructure components support it rather than replacing the individual W stages.

---

## W1 — Weather Data Collection and Cleaning

W1 establishes the initial weather-data preparation layer.

The module contains:

- Data download logic
- Cleaning logic
- Configuration
- Main execution entry point
- Raw and processed data directories

Primary technologies:

- Python
- Pandas

---

## W2 — Weather ETL Pipeline

W2 converts the cleaned input into a structured downstream-ready dataset.

The module separates:

- Extract
- Transform
- Validate
- Load
- Configuration
- Main execution

This establishes the classic ETL pattern used throughout the project.

---

## W3 — PostgreSQL Loader

W3 introduces relational persistence.

Responsibilities include:

- Database configuration
- Database connection handling
- Loading weather data
- Validating the database load

PostgreSQL becomes the structured data store used by later pipeline/orchestration stages.

---

## W4 — Apache Airflow Orchestration

W4 moves the weather pipeline into a scheduled/orchestrated workflow.

The project uses Airflow to manage task dependencies and execute the data pipeline in a reproducible order.

Phase 2 migrated the Airflow platform into Kubernetes and extended its lifecycle so that it can coordinate the complete W1-W10 processing model.

The current Airflow deployment includes:

- Airflow Init
- Airflow API Server
- Airflow Scheduler
- Airflow DAG Processor
- Project DAG
- Project orchestration code

The main DAG is:

```text
dags/weather_etl_dag.py
```

---

## W5 — PySpark ETL

W5 introduces Apache Spark as the distributed-processing component of the project.

It includes:

- PySpark ETL
- Spark SQL analysis
- Spark transformation/loading code
- A notebook for Spark ETL analysis
- A real-data comparison test between PySpark and Pandas

PySpark is used specifically for the **data-processing/ETL stage**. The W8 prediction model remains a Scikit-learn workflow; Spark MLlib is not currently used as a replacement for the W8 model.

This distinction is intentional: the project demonstrates both conventional Python data processing and distributed Spark processing without claiming that every stage must use Spark.

---

## W6 — Dashboard and Object Storage

W6 originally established the dashboard and MinIO-based object-storage layer.

The repository contains:

```text
w6_dashboard_minio/
├── src/
│   ├── data_loader.py
│   ├── minio_client.py
│   ├── upload_to_minio.py
│   ├── dashboard.py
│   └── ...
└── data/
```

MinIO provides an S3-compatible object-storage interface for the local/earlier architecture.

During Phase 2, AWS S3 became the cloud artifact store used by the deployed W1-W10 pipeline.

---

# AWS S3 Artifact Architecture

AWS S3 is now an important part of the deployed Phase 2 data/ML architecture.

The configured cloud storage environment uses:

```text
AWS Region:
eu-west-2

Bucket:
weather-data-lake-mlops
```

AWS S3 is used for **pipeline-generated artifacts**, not as a replacement for PostgreSQL.

The deployed pipeline successfully generated and uploaded the following artifacts:

```text
features/w7_features_final.parquet

models/best_model.pkl
models/scaler.pkl
models/model_metrics.json

predictions/weather_predictions.csv
```

## S3 responsibilities

The project uses AWS S3 for:

1. Uploading the W7 engineered feature dataset.
2. Uploading the trained/best model artifact.
3. Uploading the scaler used by the prediction workflow.
4. Uploading model evaluation metrics.
5. Uploading W9 batch prediction results.
6. Providing the current artifacts to the deployed FastAPI application.
7. Providing the current artifacts to the Dashboard.
8. Refreshing application Pods when new pipeline artifacts are produced.
9. Verifying that the deployed application is using the latest pipeline outputs.
10. Supporting the future MLflow/model-lifecycle architecture planned for P2-W6.

The cloud-storage utility is located at:

```text
orchestration/cloud_storage.py
```

and the repository includes:

```text
orchestration/test_cloud_storage.py
```

for cloud-storage validation.

---

## S3 Artifact Refresh

The deployed FastAPI and Dashboard workloads use Kubernetes init containers to retrieve the current artifacts from S3 before the application container starts.

The application downloads:

```text
models/best_model.pkl
models/scaler.pkl
models/model_metrics.json
features/w7_features_final.parquet
predictions/weather_predictions.csv
```

The deployment uses AWS CLI operations equivalent to:

```text
aws s3 cp s3://<bucket>/models/best_model.pkl ...
aws s3 cp s3://<bucket>/models/scaler.pkl ...
aws s3 cp s3://<bucket>/models/model_metrics.json ...
aws s3 cp s3://<bucket>/features/w7_features_final.parquet ...
aws s3 cp s3://<bucket>/predictions/weather_predictions.csv ...
```

The actual bucket name and credentials are supplied through Kubernetes configuration rather than hard-coded into the application.

### Why this matters

A container image contains the application code and dependencies, while S3 contains the current data/model artifacts.

This separates:

- **application versioning** → GHCR image
- **data/model artifacts** → AWS S3
- **relational state** → PostgreSQL
- **persistent local object-storage state** → MinIO PVC

This separation is important for updating models/data without rebuilding the entire application image.

## S3-to-Application Flow

```text
Airflow W1-W10
      ↓
Generate features / model / predictions
      ↓
AWS S3
      ↓
refresh_applications()
      ↓
Kubernetes replacement Pods
      ↓
S3 download init containers
      ↓
FastAPI / Dashboard
      ↓
Current model + current data + current predictions
```

This is one of the most important architecture flows because it connects the data pipeline to the deployed application.

---

# Machine Learning

## W7 — Feature Engineering

W7 transforms processed weather data into a feature dataset suitable for machine learning.

The final feature artifact is:

```text
w7_features_final.parquet
```

The project uses Pandas/PyArrow-based feature processing.

The engineered feature dataset is then consumed by W8.

---

## W8 — Model Training and Evaluation

W8 is the model-development stage.

The repository contains:

```text
w8_weather_prediction_model/
├── src/
│   ├── compare_models.py
│   ├── config.py
│   ├── evaluate.py
│   ├── main.py
│   └── predict.py
├── models/
│   ├── best_model.pkl
│   ├── linear_regression_model.pkl
│   ├── random_forest_model.pkl
│   ├── scaler.pkl
│   └── model_metrics.json
└── figures/
```

The model-development workflow includes:

1. Load engineered features.
2. Prepare the ML dataset.
3. Train regression models.
4. Compare model performance.
5. Evaluate predictions.
6. Persist the selected/best model.
7. Persist the scaler where required.
8. Persist model metrics.
9. Make the resulting artifacts available to the downstream W9 pipeline.

### Current validated model

The latest deployed Phase 2 validation showed:

```text
Model:        Linear Regression
R² Score:     0.99
RMSE:         0.52 °C
MAE:          0.37 °C
```

The latest cloud validation used:

```text
43,920 engineered feature records
```

and the deployed Dashboard displayed:

```text
Last Trained: 04 Sep 2026 23:12
```

The dataset size can change when the pipeline is refreshed; the figures above are the latest validated cloud-deployment snapshot rather than a claim that the dataset is permanently fixed at that size.

Earlier Phase 1/W8 training snapshots used a smaller dataset and produced different metrics. The README therefore treats the **latest validated cloud result** as the current deployment reference.

### Model artifacts

The current artifact set includes:

```text
best_model.pkl
linear_regression_model.pkl
random_forest_model.pkl
scaler.pkl
model_metrics.json
```

The presence of both Linear Regression and Random Forest artifacts reflects the model-comparison workflow. The currently validated deployed model is Linear Regression.

---

# W9 — Batch Prediction

W9 separates prediction generation from model training.

**Batch prediction** means generating predictions for a prepared dataset in one offline processing job, rather than calculating one prediction only when an individual API request arrives.

The W9 workflow:

1. Loads the engineered W7 feature dataset.
2. Loads the trained W8 model.
3. Loads the required scaler/artifacts.
4. Generates predictions for the prepared feature records.
5. Evaluates the predictions.
6. Saves the prediction output.
7. Publishes the prediction artifact for downstream use.

The prediction artifact is:

```text
predictions/weather_predictions.csv
```

The W9 repository contains:

```text
load_features.py
load_model.py
predict.py
evaluate_predictions.py
save_predictions.py
upload_to_minio.py
```

The project therefore demonstrates both:

- **Batch/offline inference:** W9
- **Application/API prediction serving:** W10

---

# W10 — FastAPI and Plotly Dash

W10 provides the application layer.

## FastAPI

FastAPI loads the deployed model artifacts and exposes prediction functionality through an HTTP API.

The service contains:

```text
w10_fastapi_service/app/
├── config.py
├── main.py
├── model_loader.py
├── predictor.py
├── routes.py
└── schemas.py
```

The service uses the model, scaler, metrics, feature and prediction artifacts downloaded from S3.

## Dashboard

The Plotly Dash application provides the presentation layer.

The Dashboard can consume:

- Current model metrics
- Engineered feature data
- Prediction results
- API responses
- Current S3-backed artifacts

The dashboard module contains separate data-loading, API-client, callback, layout, style and live-prediction components.

During cloud validation, the Dashboard successfully loaded refreshed S3 artifacts after Kubernetes application Pods were replaced.

---

# Data Quality and Archive Recovery

Phase 2 added an explicit historical archive-gap detection capability.

The project contains:

```text
orchestration/check_archive.py
```

This component was reconstructed during P2-W2 and is responsible for detecting missing historical archive periods so the pipeline can identify gaps rather than assuming that the available data is complete.

This supports a more production-oriented ingestion design:

```text
Expected historical coverage
        ↓
Archive validation
        ↓
Gap detection
        ↓
Recovery / reprocessing path
        ↓
Complete dataset
```

Comprehensive testing of archive gaps, recovery branches and archive completeness is scheduled in P2-W7.

---

# Phase 2 — Cloud-Native Platform Engineering

Phase 2 extends the Phase 1 W1-W10 project rather than replacing it.

The objective is to turn the existing pipeline into a reproducible cloud-native platform with:

- Kubernetes
- K3s
- Oracle Cloud
- Persistent storage
- Secrets
- Resource management
- AWS S3 artifacts
- Container image consolidation
- CI/CD
- Immutable image versions
- Automated deployment
- Rollback/recovery

## Phase 2 progression

| Phase | Focus | Status |
|---|---|---|
| P2-W1 | Kubernetes Foundation + Airflow/W1-W9 Migration | Complete |
| P2-W2 | Platform Consolidation + W10 Integration | Complete |
| P2-W3 | Cloud / K3s Deployment | Complete |
| P2-W4 | CI/CD | D1-D4 Complete; D5 rollback/recovery pending validation |
| P2-W5 | Public Deployment | Planned |
| P2-W6 | MLflow + Platform Optimisation | Planned |
| P2-W7 | Comprehensive Testing | Planned |
| P2-W8 | Monitoring + Final Integration | Planned |

---

# P2-W1 — Kubernetes Foundation

P2-W1 established the Kubernetes foundation and migrated the existing W1-W9/Airflow platform.

Completed areas included:

- K3s / Kubernetes foundation
- `kubectl`
- Kubernetes node readiness
- PostgreSQL StatefulSet
- PostgreSQL PVC
- PostgreSQL Service
- MinIO StatefulSet
- MinIO PVC
- MinIO Service
- Airflow migration
- Unified Airflow/project image at that stage
- W1-W9 integration
- Kubernetes RBAC
- Kubernetes Secret configuration
- End-to-end validation

The P2-W1 final validation also verified S3/artifacts and synchronization with W10.

---

# P2-W2 — Platform Consolidation + W10 Integration

P2-W2 established the canonical project image.

The Dockerfile was moved to the project root and became the single canonical build definition:

```text
Dockerfile
```

The unified image contains the dependencies and project code required by:

- Airflow
- W1-W9
- PySpark
- Machine learning
- W10 FastAPI
- Plotly Dash
- Orchestration utilities

The same root Dockerfile is used for the Docker/Kubernetes platform rather than maintaining a separate CI-only Dockerfile.

P2-W2 also:

- Validated the unified image.
- Reconstructed `check_archive.py`.
- Added historical archive-gap detection.
- Integrated W10 into the Airflow/Kubernetes lifecycle.
- Validated the complete W1-W10 execution model.

---

# P2-W3 — Oracle Cloud / K3s Deployment

The consolidated platform was deployed to an Oracle Cloud ARM64 VM.

## Oracle environment

```text
Instance:
weather-platform-k3s

Operating system:
Ubuntu 24.04.4 LTS Minimal

Architecture:
ARM64

Resources:
1 OCPU
6 GB RAM
~45 GB disk

Kubernetes:
K3s

K3s version:
v1.36.x
```

The Oracle environment was configured with:

- SSH access
- Cloud networking
- DNS/network configuration
- Swap
- K3s
- kubectl/K3s Kubernetes access
- Kubernetes workloads
- Resource requests/limits
- Persistent storage
- Secrets
- Services
- RBAC

The project uses the Oracle VM's available CPU/memory resources as the cloud execution environment.

## Deployed workloads

The validated K3s platform includes:

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

P2-W3 final validation confirmed that the W1-W10 pipeline could execute on the deployed K3s platform, produce fresh AWS S3 artifacts, and refresh the application layer.

---

# Kubernetes and Oracle Cloud

Kubernetes is responsible for running and managing the platform workloads.

It provides:

- Pods
- Deployments
- StatefulSets
- Services
- PersistentVolumeClaims
- Resource requests and limits
- Secrets
- RBAC
- Pod replacement
- Rollout management
- Service discovery

K3s provides the lightweight Kubernetes distribution used on the Oracle VM.

## Stateful workloads

PostgreSQL and MinIO use StatefulSets with persistent storage.

The application workloads use Deployments:

- Airflow components
- FastAPI
- Dashboard

This separation reflects the difference between persistent stateful services and replaceable application Pods.

---

# Docker and Platform Consolidation

The root `Dockerfile` is the canonical project image definition.

The repository also contains:

```text
docker-compose.yml
docker-compose.resolved.yml
docker_requirements.txt
```

The unified image allows the same project code/dependency environment to be used across the platform's Docker and Kubernetes workflows.

This reduced the previous separation between an Airflow-specific image and the application components.

---

# CI/CD

P2-W4 establishes a Git-driven deployment path.

The target workflow is:

```text
Git push
   ↓
GitHub Actions
   ↓
Validation + tests
   ↓
Unified Docker build
   ↓
Immutable Git-SHA image
   ↓
GHCR
   ↓
Oracle K3s
   ↓
Kubernetes rollout
```

This is the second important architecture flow in the README because it describes how a code change reaches production infrastructure.

## P2-W4 D1 — CI foundation

Completed capabilities:

- `.github/workflows/ci.yml`
- Push trigger for `main`
- Pull-request trigger for `main`
- GitHub-hosted Ubuntu runner
- Python 3.11
- Repository structure validation
- Successful real Git-triggered workflow execution

## P2-W4 D2 — Validation and image build

The CI workflow was extended to:

- Install the limited test dependencies required by the current CI test layer.
- Run `tests/test_project_imports.py`.
- Validate the repository structure.
- Build the existing root `Dockerfile`.
- Avoid creating a separate CI-specific Dockerfile.

Current test command:

```text
python -m unittest tests/test_project_imports.py
```

The CI build validates the unified project image before later publishing/deployment stages.

## P2-W4 D3 — GHCR and immutable versioning

GitHub Container Registry was configured for the project.

The image is versioned using the Git commit SHA:

```text
ghcr.io/gaurav-dwivedi-de/data_engineering_portfolio:<commit-sha>
```

A verified published image example from D3 was:

```text
ghcr.io/gaurav-dwivedi-de/data_engineering_portfolio:5d9218b782bc2441aa392d772304073bfb99b15d
```

The commit SHA makes the deployment artifact traceable to an exact source revision.

The CI build supports:

```text
linux/amd64
linux/arm64
```

This is required because GitHub-hosted build infrastructure and the Oracle ARM64 environment can use different CPU architectures.

## P2-W4 D4 — Automated Oracle deployment

The CI/CD workflow was extended from image publication to Oracle K3s deployment.

The deployment uses GitHub Actions secrets for Oracle access and connects to the Oracle VM to synchronise the repository and apply Kubernetes manifests.

The deployment process includes:

1. Synchronise the repository.
2. Verify the `weather-env` Secret exists.
3. Apply PostgreSQL PVC/StatefulSet/Service.
4. Wait for PostgreSQL readiness.
5. Apply MinIO PVC/StatefulSet/Service.
6. Wait for MinIO readiness.
7. Run Airflow initialization.
8. Apply Airflow components.
9. Apply FastAPI.
10. Apply Dashboard.
11. Apply the relevant Kubernetes Services.
12. Wait for/validate workload rollouts.

Normal deployment operations use Kubernetes `apply` semantics and do not intentionally delete the PostgreSQL or MinIO PVCs.

## P2-W4 D5 — Rollback and recovery

The remaining P2-W4 objective is to demonstrate that a known-good immutable image can be restored after a bad release.

Planned validation:

1. Identify a known-good image SHA.
2. Deploy a newer version.
3. Validate the new Kubernetes rollout.
4. Roll back to the previous image version.
5. Verify the workloads recover.
6. Confirm application functionality after rollback.

The use of immutable Git-SHA images makes this rollback model possible without relying on an ambiguous `latest` tag.

---

# Storage and Persistence

The platform deliberately uses different storage technologies for different purposes.

| Storage | Role |
|---|---|
| PostgreSQL | Structured relational weather/application data |
| MinIO | S3-compatible object storage used by the local/earlier platform and retained in Kubernetes |
| AWS S3 | Cloud storage for pipeline-generated ML/data artifacts |
| Kubernetes PVCs | Persistent local storage for stateful PostgreSQL and MinIO workloads |
| Local filesystem / `emptyDir` | Temporary application artifact staging inside Pods |

## PostgreSQL persistence

PostgreSQL is deployed as a StatefulSet with a PersistentVolumeClaim.

Its persistent storage survives normal application Pod replacement.

## MinIO persistence

MinIO is also deployed as a StatefulSet with a PersistentVolumeClaim.

Its storage survives normal Pod replacement unless the persistent storage itself is deliberately removed.

## S3 versus PVCs

AWS S3 and Kubernetes PVCs serve different purposes:

- **S3:** cloud artifact/data storage and cross-Pod artifact retrieval.
- **PVC:** persistent storage attached to Kubernetes workloads, especially PostgreSQL and MinIO.

The project therefore does not treat S3 as a database replacement.

---

# Secrets and Configuration

Sensitive configuration is supplied through Kubernetes Secrets rather than being embedded in application code.

The main Kubernetes Secret is:

```text
weather-env
```

The Secret is used for configuration such as:

- Database credentials
- AWS/S3 credentials
- S3 bucket configuration
- Other runtime configuration

CI/CD also uses GitHub repository secrets for Oracle deployment credentials, including the SSH key used by GitHub Actions.

Sensitive values should never be committed to the repository.

The repository should contain configuration references and Kubernetes manifests, not secret values.

---

# Networking and Service Exposure

Kubernetes Services provide internal communication between the platform workloads.

The deployed platform uses Kubernetes networking for communication between:

- Airflow
- PostgreSQL
- MinIO
- FastAPI
- Dashboard

FastAPI and Dashboard have their own Kubernetes Services.

P2-W3 also validated external access for the Dashboard during cloud deployment. Formal public deployment with a project domain, Kubernetes Ingress and HTTPS/TLS remains part of P2-W5.

This distinction is important:

- **P2-W3:** cloud deployment and validated external/service access.
- **P2-W5:** formal public deployment, DNS, Ingress, HTTPS/TLS and secure public routing.

---

# Application Refresh and Artifact Synchronisation

One of the more important Phase 2 behaviours is automatic application refresh after the pipeline generates new artifacts.

The Airflow orchestration includes:

```text
refresh_applications()
```

After fresh artifacts are uploaded to S3, this task causes FastAPI and Dashboard Deployments to create replacement Pods.

Their S3 download init containers retrieve the latest artifacts before the application containers start.

During P2-W3 validation, the application successfully loaded refreshed data including:

```text
Loaded 43920 feature rows.
Loaded 43848 prediction rows.
```

and the Dashboard reported:

```text
All Dashboard S3 files downloaded successfully.
```

This resolved the earlier stale-data issue where new S3 artifacts could exist without already-running application Pods automatically reloading them.

---

# Testing and Validation

Testing is being expanded incrementally.

## Current CI tests

The current CI test layer includes:

```text
tests/test_project_imports.py
```

The test verifies that core dependencies required by the current validation layer can be imported, including:

- NumPy
- Pandas
- Requests
- Scikit-learn
- Joblib

The CI workflow also verifies the expected repository structure and builds the unified Docker image.

## Existing project tests

The repository contains additional tests across the project, including:

```text
w5_spark_weather_etl/tests/
w7_feature_engineering/test_check_dataset.py
w9_ml_pipeline/
w10_fastapi_service/tests/
orchestration/test_cloud_storage.py
```

The repository structure also contains validation modules for W1-W4 and W3 database loading.

## Phase 2 comprehensive testing

P2-W7 is planned to expand validation across:

- W1-W10 components
- Data quality
- Archive-gap detection
- Recovery branches
- Archive completeness
- PostgreSQL
- MinIO
- AWS S3
- Airflow
- Kubernetes
- FastAPI
- Dashboard
- Complete W1-W10 end-to-end execution

The roadmap specifically includes testing W10 against fresh S3 artifacts and current prediction outputs.

---

# Technology Stack

## Data Engineering

- Python
- Pandas
- NumPy
- PyArrow
- PostgreSQL
- PySpark
- Spark SQL
- Apache Airflow

## Storage

- PostgreSQL
- MinIO
- AWS S3
- Boto3 / AWS CLI
- Kubernetes PersistentVolumes / PersistentVolumeClaims

## Machine Learning

- Scikit-learn
- Joblib
- Linear Regression
- Random Forest
- Regression evaluation metrics: R², RMSE, MAE

## Application

- FastAPI
- Uvicorn
- Plotly Dash

## Infrastructure

- Docker
- Docker Compose
- Kubernetes
- K3s
- Oracle Cloud
- Kubernetes Services
- Kubernetes Deployments
- Kubernetes StatefulSets
- Kubernetes PVCs
- Kubernetes RBAC
- Kubernetes Secrets

## CI/CD

- GitHub
- GitHub Actions
- GitHub Container Registry
- Docker Buildx
- QEMU
- Multi-platform Docker images
- Git commit-SHA image versioning

## Planned MLOps

- MLflow
- Experiment tracking
- Model artifact tracking
- Model versioning/lifecycle management

---

# Repository Structure

The current repository contains the core W1-W10 modules, orchestration utilities, Kubernetes manifests, deployment material, tests, and Phase 2 development notes.

```text
data_engineering_portfolio/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── dags/
│   └── weather_etl_dag.py
│
├── orchestration/
│   ├── check_archive.py
│   ├── cloud_storage.py
│   ├── config.py
│   ├── create_db.py
│   └── test_cloud_storage.py
│
├── tests/
│   └── test_project_imports.py
│
├── k8/
│   ├── airflow/
│   │   ├── airflow-init.yaml
│   │   ├── api-server.yaml
│   │   ├── dag-processor.yaml
│   │   ├── rbac.yaml
│   │   └── scheduler.yaml
│   ├── dashboard/
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   ├── fastapi/
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   ├── minio/
│   │   ├── deploy_minio.sh
│   │   ├── pvc.yaml
│   │   ├── service.yaml
│   │   └── statefulset.yaml
│   └── postgres/
│       ├── deploy_postgres.sh
│       ├── pvc.yaml
│       ├── service.yaml
│       └── statefulset.yaml
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
├── w11_deployment/
│
├── config/
├── changelog_notes/
│   ├── P2-W2/
│   └── P2-W3/
│
├── Dockerfile
├── docker-compose.yml
├── docker-compose.resolved.yml
├── docker_requirements.txt
├── k8-commands.md
├── requirements.txt
└── README.md
```

The full repository also contains module-specific READMEs, figures, notebooks, deployment screenshots and supporting files.

The current repository inventory contains approximately **73 directories and 156 files**, including the W1-W10 modules, Kubernetes manifests and supporting project documentation.

---

# Development and Deployment Workflow

## Local development

The normal development workflow is:

```text
VS Code
   ↓
Local testing
   ↓
GitHub Desktop
   ↓
Commit
   ↓
Push to GitHub
```

GitHub Desktop is used for reviewing, committing and pushing project changes.

## CI/CD workflow

After a qualifying Git push:

```text
GitHub
   ↓
GitHub Actions
   ↓
Repository validation
   ↓
Automated tests
   ↓
Unified Docker build
   ↓
GHCR image
   ↓
Oracle Cloud K3s
   ↓
Kubernetes rollout
```

The final intended developer experience is:

**change code → test locally → commit/push → CI validates → immutable image is published → Oracle K3s is updated.**

---

# Current Status

## Phase 1

| Stage | Status |
|---|---|
| W1 | Complete |
| W2 | Complete |
| W3 | Complete |
| W4 | Complete |
| W5 | Complete |
| W6 | Complete |
| W7 | Complete |
| W8 | Complete |
| W9 | Complete |
| W10 | Complete |

Phase 1 established the working data engineering, ML, API and Dashboard platform.

---

## Phase 2

### P2-W1 — Kubernetes Foundation

**Complete**

Established:

- Kubernetes/K3s foundation
- PostgreSQL StatefulSet + PVC
- MinIO StatefulSet + PVC
- Airflow on Kubernetes
- W1-W9 integration
- Kubernetes RBAC
- Kubernetes Secrets
- End-to-end validation

### P2-W2 — Platform Consolidation

**Complete**

Established:

- Root canonical Dockerfile
- Unified W1-W10 project image
- Docker Compose/Kubernetes reuse
- `check_archive.py`
- Historical archive-gap detection
- W10 integration with the Airflow/Kubernetes lifecycle

### P2-W3 — Cloud/K3s Deployment

**Complete**

Validated:

- Oracle Cloud ARM64 environment
- K3s
- PostgreSQL persistence
- MinIO persistence
- Airflow
- FastAPI
- Dashboard
- Kubernetes resource management
- Kubernetes Services
- Secrets
- AWS S3 artifact storage
- Fresh W1-W10 execution
- S3 artifact generation
- Automatic application refresh
- Updated model/data consumption

The final P2-W3 validation demonstrated the chain:

```text
Airflow
  ↓
W1-W10
  ↓
AWS S3 artifacts
  ↓
Application refresh
  ↓
FastAPI / Dashboard
```

---

## P2-W4 — CI/CD

### Completed

- D1 — CI workflow and Git-based triggers
- D2 — Automated validation, limited tests and unified Docker build
- D3 — GHCR and immutable Git-SHA image versioning
- D4 — Automated Oracle K3s deployment and Kubernetes rollout

### Remaining

- D5 — Kubernetes rollback/recovery validation

The current CI/CD architecture therefore has the main path operational, with rollback/recovery remaining as the final P2-W4 validation objective.

---

# Roadmap

The Phase 2 roadmap is dependency-driven.

## P2-W4 — CI/CD

**D5 — Rollback / Recovery**

- Deploy a known-good image.
- Deploy a newer image.
- Validate rollout.
- Roll back to the previous image.
- Validate recovery and application functionality.

## P2-W5 — Public Deployment

Scheduled work:

| Day | Task | Date |
|---|---|---|
| D1 | Project domain and DNS | 14/09/2026 |
| D2 | Kubernetes Ingress | 15/09/2026 |
| D3 | HTTPS/TLS | 16/09/2026 |
| D4 | Public FastAPI + Dashboard | 17/09/2026 |
| D5 | Secure public access and service routing | 18/09/2026 |

## P2-W6 — MLflow + Platform Optimisation

Scheduled work:

| Day | Task | Date |
|---|---|---|
| D1 | Integrate MLflow with W8/W9 | 21/09/2026 |
| D2 | Track experiments, parameters, metrics and artifacts | 22/09/2026 |
| D3 | Model versioning/lifecycle with existing S3 architecture | 23/09/2026 |
| D4 | Review Spark, ML, Kubernetes, image, storage and dependency efficiency | 24/09/2026 |
| D5 | Validate W8 → W9 → MLflow and implement necessary optimisations | 25/09/2026 |

The current plan is to optimise only where there is a demonstrated engineering benefit rather than replacing working components simply to add technologies.

## P2-W7 — Comprehensive Testing

Scheduled work:

| Day | Task | Date |
|---|---|---|
| D1 | W1-W10 and core data-quality testing | 28/09/2026 |
| D2 | Archive gaps, recovery branches and completeness | 29/09/2026 |
| D3 | PostgreSQL, MinIO/S3, Airflow, Kubernetes and integration testing | 30/09/2026 |
| D4 | FastAPI/Dashboard against fresh S3 artifacts and predictions | 01/10/2026 |
| D5 | Production-style W1-W10 E2E test and failure resolution | 02/10/2026 |

## P2-W8 — Monitoring + Final Integration

Scheduled work:

| Day | Task | Date |
|---|---|---|
| D1 | Airflow and pipeline execution monitoring | 05/10/2026 |
| D2 | Kubernetes, resources, PostgreSQL and MinIO monitoring | 06/10/2026 |
| D3 | FastAPI and Dashboard availability/failure monitoring | 07/10/2026 |
| D4 | Final W1-W10 execution and complete lineage verification | 08/10/2026 |
| D5 | Final architecture, deployment documentation, portfolio presentation and cleanup | 09/10/2026 |

These dates and work packages follow the current Phase 2 project plan. fileciteturn0file2

---

# Important Architecture Decisions

## 1. Airflow is the orchestrator, not the infrastructure layer

Airflow coordinates the W1-W10 workflow.

Kubernetes runs the services.

This keeps orchestration and infrastructure responsibilities separate.

## 2. PostgreSQL is not replaced by S3

PostgreSQL provides relational storage.

AWS S3 provides object storage for datasets, models, metrics and predictions.

They solve different problems.

## 3. MinIO and AWS S3 have different roles

MinIO was introduced as S3-compatible object storage during Phase 1 and remains deployed as a Kubernetes service with persistent storage.

AWS S3 is the cloud object store used by the deployed Phase 2 artifact workflow.

The project therefore demonstrates both local/S3-compatible object storage and cloud object storage.

## 4. The Docker image and ML artifacts are versioned differently

Application code and dependencies are versioned through immutable Git commit-SHA container images.

ML/data artifacts are stored separately in S3.

This avoids rebuilding the application image every time a model or dataset changes.

## 5. PySpark is used where distributed processing is relevant

W5 demonstrates Spark ETL and Spark SQL.

W8 continues to use Scikit-learn for the current regression model.

The project does not claim that Spark automatically improves the W8 model simply by replacing Scikit-learn.

## 6. Batch prediction and API prediction are different workloads

W9 performs offline batch prediction over a prepared dataset.

W10 provides application/API access to predictions.

This separation makes the ML pipeline easier to orchestrate and the application layer easier to deploy.

## 7. `latest` is not the deployment identity

The CI/CD architecture moves toward immutable Git-SHA image references.

A deployment can therefore be tied to a precise source revision, which is required for reliable rollback.

---

# Known Scope and Limitations

The project is intentionally developed incrementally.

Current limitations include:

- The CI test suite is still smaller than the full project test surface.
- Comprehensive W1-W10 E2E testing is scheduled for P2-W7.
- MLflow is not yet integrated; it is planned for P2-W6.
- Formal public Ingress/HTTPS deployment is planned for P2-W5.
- Kubernetes rollback/recovery is the remaining P2-W4 validation objective.
- Monitoring is planned for P2-W8.
- Spark is currently demonstrated in W5 rather than replacing the Scikit-learn W8 model.
- The Oracle deployment uses a small ARM64 Free Tier VM, so resource management is an explicit engineering constraint.

These are roadmap items, not missing definitions of the existing platform.

---

# Documentation

The repository contains implementation documentation alongside the code.

Important documentation locations include:

```text
README.md

workflow.md

k8/README.md
k8-commands.md

w1_weather_data_cleaner/README.md
w2_weather_etl_pipeline/README.md
w3_postgresql_loader/README.md
w4_airflow_weather_pipeline/README.md
w5_spark_weather_etl/README.md
w6_dashboard_minio/README.md
w7_feature_engineering/README.md
w8_weather_prediction_model/README.md
w9_ml_pipeline/README.md
w10_fastapi_service/README.md
w11_deployment/README.md

changelog_notes/
├── P2-W2/
└── P2-W3/
```

The Phase 2 daily notes document implementation details, commands, problems, decisions and validation results.

The current repository structure confirms the presence of the W1-W10 modules, orchestration utilities, Kubernetes manifests, W11 deployment material, tests and supporting configuration. fileciteturn0file1

---

# Project Objective

The objective is to demonstrate how a real data/ML workflow can evolve from a local engineering project into a cloud-native platform.

The project progression is:

```text
Data Engineering
      ↓
ETL + Database
      ↓
Workflow Orchestration
      ↓
Distributed Processing
      ↓
Feature Engineering
      ↓
Machine Learning
      ↓
Batch Prediction
      ↓
API + Dashboard
      ↓
Docker
      ↓
Kubernetes
      ↓
Oracle Cloud
      ↓
AWS S3 Artifacts
      ↓
CI/CD
      ↓
Immutable Deployments
      ↓
Rollback / Recovery
      ↓
Public Deployment
      ↓
MLflow
      ↓
Comprehensive Testing
      ↓
Monitoring + Final Integration
```

The project is designed to demonstrate **engineering integration** rather than isolated technology usage.

The final platform is intended to provide a reproducible path from raw weather data through processing and machine learning to a deployed prediction application, with orchestration, storage, infrastructure, CI/CD, testing and monitoring surrounding the complete lifecycle.
