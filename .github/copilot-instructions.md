# Weather Intelligence Platform — Git Commit Instructions

Generate Git commit messages for this repository using the rules below.

The repository is the Weather Intelligence Platform, an integrated data engineering, MLOps, ML, and platform engineering portfolio project.

The project uses a W# D# workflow:
- W# = project week
- D# = day/task within that week
- Phase 1 = W1–W12
- Phase 2 = P2-W1, P2-W2, etc.

Do not invent a W# D# or Phase 2 task when it cannot be determined from the changes.

## 1. Commit title

Use this format:

<type>(<scope>): <short imperative description>

Maximum length: 72 characters.

Use these Conventional Commit types:

- feat: new functionality
- fix: bug fix
- refactor: code restructuring without changing intended behavior
- test: tests or validation
- docs: documentation
- chore: dependencies, configuration, or maintenance
- deploy: deployment or infrastructure changes
- perf: performance improvements
- ci: CI/CD changes

Use the most specific appropriate type.

Use a scope that identifies the affected component when useful.

Examples:

feat(k8s): deploy FastAPI service
fix(api): correct prediction response validation
feat(airflow): update weather pipeline
deploy(oci): configure cloud deployment
docs(k8s): document deployment commands
test(api): validate prediction responses
chore(docker): update Airflow image

Title rules:
- Use imperative language.
- Be specific about the actual change.
- Maximum 72 characters.
- Do not end with a period.
- Do not use vague wording such as "update files", "make changes", or "misc changes".
- Do not include information that is not supported by the Git diff.

## 2. Commit description format

The commit description MUST be written line by line.

Use a separate bullet beginning with `-` for every point.

Required visual format:

- <project task or primary change>
- <technical change>
- <technical purpose or impact>
- <validation or additional important change>

Do NOT combine multiple points into one paragraph.

Do NOT use numbered lists.

Do NOT use a single long paragraph.

Do NOT use blank lines between description bullets.

Example:

feat(k8s): deploy FastAPI service
- W11 D3: Added the FastAPI Kubernetes Deployment.
- Added the Kubernetes Service configuration.
- Configured environment variables required by the API.
- Prepared the API for cluster-based deployment.

## 3. Description length

Generate 2–4 description lines.

Each line must:
- Begin with `-`.
- Contain one clear piece of information.
- Normally stay below 120 characters.
- Describe an actual change visible in the Git diff.
- Be technically specific.
- Explain the purpose or impact when useful.

Prefer 3 lines when the change is simple.

Use 4 lines when additional clarity is required.

Do not add unnecessary lines merely to reach four bullets.

## 4. Description clarity

Every description line must communicate a distinct point.

Prefer:

- W11 D3: Added the FastAPI Kubernetes Deployment.
- Configured environment variables for the API container.
- Added a Kubernetes Service for internal API access.
- Prepared the service for cluster deployment.

Avoid:

- Updated Kubernetes files.
- Made some deployment changes.
- Updated configuration and other files.
- Improved the deployment.

The description should allow someone reviewing the Git history to understand the change without opening every changed file.

## 5. Project task reference

When the changes clearly correspond to a project task, include the relevant W# D# reference.

Examples:

- W11 D3
- W11 D4
- P2-W1 D2
- P2-W2 D4

Place the task reference in the first description line when appropriate.

Example:

- W11 D3: Added the FastAPI Kubernetes Deployment.
- Configured the API container environment.
- Added the Kubernetes Service configuration.

Do not invent a W# D# or P2-W# D# reference.

If the exact task cannot be determined reliably from the available context and changes, omit the reference.

## 6. Determine the project task

Before generating the commit message, inspect:

1. Git diff.
2. Changed file paths.
3. Changed directories.
4. README or documentation changes.
5. Configuration changes.
6. Relevant project context.

Use the actual changes as the primary source of truth.

Do not assign a task based only on the filename.

Do not infer a task simply because a file belongs to a particular week.

## 7. Weather Intelligence Platform project structure

Recognize these project areas when generating commit messages.

### W1 — Weather Data Collection & Exploration

Weather data collection, cleaning, exploration, raw data, processed data, and foundational ingestion.

### W2 — Weather ETL Pipeline

Python ETL, extraction, transformation, loading, validation, and Dockerized ETL.

### W3 — PostgreSQL Data Loader

PostgreSQL integration, database loading, schemas, connections, and validation.

### W4 — Airflow Weather Pipeline

Airflow DAGs, scheduling, weather ingestion, transformation, loading, and orchestration.

### W5 — Spark Weather ETL

PySpark ETL, Spark transformations, Spark SQL, Parquet processing, and Pandas/Spark comparison.

### W6 — Dashboard & Cloud/Object Storage

Dash dashboard, visualization, MinIO, object storage, Parquet access, and data presentation.

### W7 — Feature Engineering

Weather feature creation, transformation, ML-ready datasets, and feature validation.

### W8 — Weather Prediction Model

Model training, model comparison, evaluation, serialization, prediction, metrics, and ML artifacts.

### W9 — ML Pipeline / MLOps

Batch inference, model loading, prediction pipelines, evaluation, prediction storage, and ML pipeline integration.

### W10 — FastAPI Service

FastAPI application, prediction endpoints, schemas, model serving, API validation, and dashboard/API integration.

### W11 — Deployment

Docker deployment, Kubernetes, FastAPI deployment, dashboard deployment, infrastructure configuration, service exposure, and public deployment work.

### W12 — Testing, Documentation & Portfolio Finalization

Final testing, documentation, architecture explanation, screenshots, portfolio presentation, cleanup, and project polishing.

## 8. Phase 2 project context

Phase 2 extends the Weather Intelligence Platform beyond the Phase 1 deployment.

Phase 2 areas may include:

- Oracle Cloud / OCI
- K3s / Kubernetes
- AWS S3
- cloud deployment
- public IP/domain
- HTTPS
- CI/CD
- automated testing
- monitoring
- data-gap detection
- MLflow
- Spark improvements
- production-oriented infrastructure

Use Phase 2 references when they are reliably known:

P2-W1
P2-W2
P2-W3
etc.

Do not confuse Phase 1 W11 Kubernetes work with Phase 2 cloud/Kubernetes work.

## 9. Preferred scopes

Use the following scopes when applicable:

- w1
- w2
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

Use the simplest accurate scope.

Do not force a scope when none is appropriate.

## 10. Technology-specific wording

Use technically accurate terminology.

Prefer:

- Added Kubernetes Deployment and Service manifests.
- Configured Kubernetes environment variables.
- Updated Airflow DAG scheduling.
- Added PostgreSQL persistence configuration.
- Configured S3 object storage.
- Added FastAPI prediction endpoint.
- Added pytest validation.
- Updated Docker image configuration.
- Added Kubernetes persistent volume configuration.
- Configured MinIO object storage.
- Added Airflow Kubernetes deployment configuration.

Avoid vague wording:

- Improved Kubernetes.
- Updated backend.
- Changed some files.
- Made deployment better.
- Updated things.
- Fixed stuff.
- Improved the project.

## 11. Testing and validation

Only mention testing when supported by the changes or available evidence.

If tests were added:

- Added pytest coverage for prediction responses.

If tests were modified:

- Updated API validation tests for the revised response schema.

If tests were actually run and the result is available:

- Verified the API prediction response against the expected output.

Do not claim that tests passed when there is no evidence that they were executed.

Do not claim successful deployment when the diff only contains deployment configuration.

## 12. Documentation commits

For documentation-only changes, use:

docs(<scope>): <specific documentation change>

Example:

docs(k8s): document deployment commands
- W11 D4: Added Kubernetes deployment and service commands.
- Documented pod, deployment, and service verification.
- Clarified the local Kubernetes deployment workflow.

Do not describe documentation changes as features.

## 13. Configuration and infrastructure commits

Use `chore`, `deploy`, or `ci` according to the actual purpose.

Examples:

deploy(k8s): configure dashboard service
chore(docker): update Airflow container configuration
ci(github): add automated test workflow

Do not use `feat` simply because infrastructure files were added.

## 14. Related changes

When several changed files form one logical task, describe them together.

Example:

feat(k8s): deploy PostgreSQL with persistent storage
- P2-W2 D3: Added the PostgreSQL StatefulSet configuration.
- Added persistent volume configuration for database storage.
- Configured the PostgreSQL Kubernetes Service.
- Added deployment settings required by the platform.

Do not list every changed filename unless the filename itself provides important context.

## 15. Unrelated changes

If a commit contains unrelated changes, do not create a misleading single-purpose description.

Describe the major related changes accurately.

Do not invent a relationship between unrelated changes.

If the changes clearly represent multiple independent tasks, describe each important task on its own line.

## 16. Documentation of impact

When useful, explain why the change matters.

Prefer:

- Added persistent storage to prevent PostgreSQL data loss during pod recreation.

Over:

- Added PVC.

However, keep the description concise.

The goal is to communicate:

WHAT changed
+
WHY it changed
+
WHAT impact it has

when that information is supported by the diff.

## 17. Final output structure

Always use this structure:

<type>(<scope>): <short imperative description>
- <line 1>
- <line 2>
- <line 3>
- <line 4>

Use only 2–4 description lines.

Do not add a separate "Description:" heading.

Do not add explanatory text before or after the commit message.

Do not use Markdown headings in the generated commit message.

Do not use numbered lists.

Every description line must start with `-`.

## 18. Examples

### Kubernetes deployment

feat(k8s): deploy FastAPI service
- W11 D3: Added the FastAPI Kubernetes Deployment.
- Added the Kubernetes Service configuration.
- Configured environment variables required by the API.
- Prepared the API for cluster deployment.

### Airflow change

feat(airflow): update weather pipeline configuration
- W4 D4: Updated the weather ETL DAG configuration.
- Adjusted pipeline scheduling and execution settings.
- Preserved the existing extraction and transformation workflow.

### ML pipeline change

fix(mlops): correct prediction pipeline loading
- W9 D4: Corrected feature loading in the batch prediction pipeline.
- Updated the model input path used during inference.
- Ensured predictions use the expected ML-ready feature dataset.

### API testing

test(api): validate prediction response
- W10 D4: Added validation for the FastAPI prediction response.
- Compared API output against the expected prediction structure.
- Added coverage for the corrected response behavior.

### Documentation

docs(k8s): document deployment workflow
- W11 D4: Added Kubernetes deployment and verification commands.
- Documented pod, deployment, and service inspection.
- Clarified the workflow for restarting deployed services.

### Phase 2 cloud infrastructure

deploy(oci): configure cloud Kubernetes resources
- P2-W1 D3: Added Kubernetes configuration for the cloud environment.
- Configured deployment resources required by the platform.
- Prepared the infrastructure for cloud-based execution.

## 19. Final quality check

Before generating the commit message, verify:

- Title is no more than 150 characters.
- Commit type accurately represents the change.
- Scope accurately identifies the affected component.
- Title uses imperative language.
- Description contains 2–4 lines.
- Every description line begins with `-`.
- Each line communicates one clear point.
- Lines are concise and normally below 120 characters.
- W# D# or P2-W# is included only when supported.
- No technical claim is invented.
- Tests are mentioned only when supported by evidence.
- No unrelated project history is included.
- No vague wording is used.
- No paragraph-style description is generated.
- No blank lines are inserted between description bullets.
