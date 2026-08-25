# Weather Intelligence Platform — Git Commit Instructions

Generate Git commit messages for this repository using the rules below.

The repository is the Weather Intelligence Platform, an integrated data engineering and MLOps portfolio project.

The project uses a W# D# workflow:
- W# = project week
- D# = day/task within that week
- Phase 1 = W1–W12
- Phase 2 = P2-W1, P2-W2, etc.

Do not invent a W# D# or Phase 2 task when it cannot be determined from the changes.

## 1. Commit title

Use:

<type>(<scope>): <imperative short description>

Maximum length: 72 characters.

Use these Conventional Commit types:

- feat: new functionality
- fix: bug fix
- refactor: code restructuring without changing intended behavior
- test: tests or validation
- docs: documentation
- chore: dependencies, configuration, maintenance
- deploy: deployment, infrastructure, or hosting changes
- perf: performance improvement
- ci: CI/CD changes

Use the most specific appropriate type.

Use a scope that identifies the affected component when useful.

Examples:

- feat(k8s): deploy FastAPI service
- fix(api): correct prediction response validation
- feat(airflow): migrate DAG configuration
- deploy(oci): configure cloud deployment
- docs(k8s): document deployment commands
- test(api): validate prediction responses
- chore(docker): update Airflow image

Rules for titles:
- Use imperative language.
- Be specific about the actual change.
- Do not end with a period.
- Do not use vague wording such as "update files", "make changes", or "misc changes".
- Do not include information that is not supported by the Git diff.

## 2. Commit description

Generate a concise technical description containing 2–4 bullet points.

Preferred structure:

- W# D#: <primary task completed>
- <important technical change>
- <technical purpose, validation, or impact>

If a W# D# reference cannot be determined reliably, omit it rather than guessing.

Each bullet should:
- Describe an actual change visible in the diff.
- Explain the technical purpose or impact when useful.
- Be specific and concise.
- Normally stay below 120 characters.
- Avoid repeating the commit title.

Do not:
- Invent changes.
- Claim that something was tested when no test evidence is present.
- Claim deployment succeeded unless the changes or repository context support that conclusion.
- Describe unrelated previous work.
- Repeat every changed filename.
- Include unnecessary implementation details.
- Use generic statements such as "updated files", "made changes", or "improved the project".

## 3. Determine the project task

Before generating the message, inspect the Git diff and changed file paths.

Use these signals to determine the relevant project task:

1. Changed directory or component.
2. File names and implementation purpose.
3. README or documentation changes.
4. Kubernetes, Docker, Airflow, PostgreSQL, MinIO, AWS, OCI, or application configuration.
5. The current W# D# context when it is explicitly present in the repository changes or task context.

Do not infer a task solely from a filename if the actual changes indicate something different.

## 4. Weather Intelligence Platform component scopes

Prefer these scopes when applicable:

- w1 / ingestion
- w2 / etl
- postgres
- airflow
- spark
- dashboard
- minio
- features
- ml
- mlops
- api
- fastapi
- k8s
- docker
- aws
- oci
- ci
- tests
- docs
- deployment

Use the simplest accurate scope. Do not force a scope when none is appropriate.

## 5. Phase 1 project context

Recognize these major project areas when generating commit messages.

### W1 — Weather Data Collection & Exploration
Weather data collection, cleaning, exploration, raw/processed data, and foundational ingestion.

### W2 — Weather ETL Pipeline
Python ETL, extraction, transformation, loading, validation, and Dockerized ETL.

### W3 — PostgreSQL Data Loader
PostgreSQL integration, database loading, schemas, connections, and validation.

### W4 — Airflow Weather Pipeline
Airflow orchestration, DAGs, scheduled weather ingestion, transformation, loading, and pipeline automation.

### W5 — Spark Weather ETL
PySpark ETL, Spark transformations, Spark SQL, Parquet processing, and comparison with Pandas.

### W6 — Dashboard & Cloud/Object Storage
Dashboard development, Dash, MinIO, object storage, Parquet data access, and visualization.

### W7 — Feature Engineering
Weather feature creation, transformation, ML-ready datasets, and feature validation.

### W8 — Weather Prediction Model
Model training, model comparison, evaluation, serialization, prediction, metrics, and ML artifacts.

### W9 — ML Pipeline / MLOps
Batch inference, model loading, prediction pipelines, evaluation, prediction storage, and ML pipeline integration.

### W10 — FastAPI Service
FastAPI application, prediction endpoints, schemas, model serving, API validation, and dashboard/API integration.

### W11 — Deployment
Containerized deployment, Docker, Kubernetes, FastAPI deployment, dashboard deployment, infrastructure configuration, and service exposure.

Phase 1 W11 is focused on local/containerized Kubernetes deployment.

### W12 — Testing, Documentation & Portfolio Finalization
Final testing, documentation, architecture explanation, screenshots, portfolio presentation, cleanup, and final project polishing.

## 6. Phase 2 context

Phase 2 extends the Weather Intelligence Platform beyond the Phase 1 local deployment.

Phase 2 may include:
- Oracle Cloud / OCI
- OKE or K3s Kubernetes deployment
- AWS S3
- public cloud deployment
- public IP/domain
- HTTPS
- CI/CD
- pytest and stronger automated testing
- monitoring
- data-gap detection
- MLflow
- Spark improvements
- production-oriented infrastructure

When a change belongs to Phase 2, use the appropriate reference when known:

- P2-W1
- P2-W2
- P2-W3
- etc.

Do not confuse Phase 1 W11 Kubernetes work with Phase 2 cloud Kubernetes work.

## 7. Technology-specific wording

Use technically accurate terminology.

Prefer:
- "Added Kubernetes Deployment and Service manifests"
- "Configured Kubernetes environment variables"
- "Updated Airflow DAG scheduling"
- "Added PostgreSQL persistence configuration"
- "Configured S3 object storage"
- "Added FastAPI prediction endpoint"
- "Added pytest validation"
- "Updated Docker image configuration"

Avoid vague wording:
- "Improved Kubernetes"
- "Updated backend"
- "Changed some files"
- "Made deployment better"

## 8. Testing and validation

Only mention testing when supported by the changes or available evidence.

Examples:

If tests were added:
- "Added pytest coverage for prediction responses."

If tests were modified:
- "Updated API validation tests for the revised response schema."

If the diff only changes application code:
- Do not claim that tests passed.

If configuration was changed:
- Describe the configuration change rather than claiming successful deployment.

## 9. Documentation commits

For documentation-only changes, use:

docs(<scope>): <specific documentation change>

Examples:

docs(k8s): document cluster deployment commands

- W11 D4: Added commands for deploying Kubernetes services.
- Documented pod, deployment, and service verification.
- Clarified the local deployment workflow.

Do not describe documentation changes as features.

## 10. Configuration and infrastructure commits

Use `chore`, `deploy`, or `ci` according to the actual purpose.

Examples:

deploy(k8s): configure dashboard service

chore(docker): update Airflow container configuration

ci(github): add automated test workflow

Do not use `feat` merely because infrastructure files were added.

## 11. Commit size

The commit message should reflect the logical unit of work represented by the diff.

If the diff contains several related changes belonging to one task, describe them together.

If the diff contains unrelated changes, describe only what can be established from the current commit.

Do not create a narrative of the entire project history.

## 12. Output format

Always generate:

<type>(<scope>): <short description>

- W# D#: <primary change>
- <technical change>
- <purpose, validation, or impact>

If no reliable W# D# is available:

<type>(<scope>): <short description>

- <primary technical change>
- <secondary technical change>
- <purpose, validation, or impact>

Keep the description to 2–4 bullets.

The final commit message should be concise, technical, factual, and suitable for a professional data engineering portfolio.

## 13. Quality check before generating

Before producing the commit message, verify:

- Is the title <=72 characters?
- Is the commit type appropriate?
- Is the scope accurate?
- Is the title imperative?
- Are all description points supported by the diff?
- Is the W# D# reference supported?
- Are there 2–4 bullets?
- Is unnecessary detail removed?
- Have vague phrases been avoided?
- Have tests only been mentioned when supported?
