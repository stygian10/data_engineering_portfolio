# Kubernetes Airflow Migration

This folder contains the Kubernetes setup for moving the Weather Intelligence
Platform from Docker Compose to Kubernetes.

The main idea is simple:

Docker Compose used to run:
- PostgreSQL
- MinIO
- Airflow
- W1-W9 through the Airflow DAG
- W10 separately

Kubernetes now runs the same architecture as separate Kubernetes resources.

The important point is that W1-W9 are NOT separate long-running Kubernetes
Deployments. Airflow runs them as pipeline tasks. The Airflow image contains
the code for W1-W9 and the DAG tells Airflow what runs first and what runs
next.

Current local setup:

Kubernetes
|
+-- PostgreSQL
|
+-- MinIO
|
+-- Airflow
|   +-- airflow-init
|   +-- API Server
|   +-- Scheduler
|   +-- DAG Processor
|   +-- LocalExecutor
|       +-- weather_etl_pipeline
|           +-- W1
|           +-- W2
|           +-- W3
|           +-- W4
|           +-- W5
|           +-- W6
|           +-- W7
|           +-- W8
|           +-- W9
|           +-- AWS S3 upload
|
+-- W10
    +-- FastAPI
    +-- Prediction Dashboard

The current local Kubernetes cluster is Docker Desktop Kubernetes.
The same manifests are intended to be used later as the basis for the K3s
deployment on Oracle Cloud.

--------------------------------------------------
1. IMPORTANT FILES
--------------------------------------------------

Expected structure:

k8/
|
+-- airflow/
|   +-- Dockerfile
|   +-- airflow-init.yaml
|   +-- api-server.yaml
|   +-- scheduler.yaml
|   +-- dag-processor.yaml
|   +-- README.md
|
+-- postgres/
|   +-- pvc.yaml
|   +-- statefulset.yaml
|   +-- service.yaml
|
+-- minio/
|   +-- pvc.yaml
|   +-- statefulset.yaml
|   +-- service.yaml
|
+-- W10 Kubernetes files
    +-- FastAPI
    +-- Prediction Dashboard

The exact W10 filenames may be different. The important thing is that W10
remains separate from the Airflow W1-W9 image for now.

--------------------------------------------------
2. BEFORE STARTING
--------------------------------------------------

Make sure:

1. Kubernetes is running.
2. PostgreSQL is running.
3. MinIO is running.
4. The Kubernetes Secret `weather-env` exists.
5. The Airflow image `airflow-custom:k8` exists.

Check Kubernetes:

    kubectl config current-context

For the current local setup this should be:

    docker-desktop

Check the cluster:

    kubectl get nodes

Check the Secret:

    kubectl get secret weather-env

Check PostgreSQL:

    kubectl get pods -l app=postgres

Check MinIO:

    kubectl get pods -l app=minio

--------------------------------------------------
3. AIRFLOW DOCKER IMAGE
--------------------------------------------------

File:

    k8/airflow/Dockerfile

This is the image used by the Kubernetes Airflow services.

Important:

Build it from the PROJECT ROOT.

Do NOT run the build from:

    w4_airflow_weather_pipeline/

Build:

    docker build -f k8/airflow/Dockerfile -t airflow-custom:k8 .

The image uses:

    apache/airflow:3.3.0-python3.11

The image contains the dependencies required by the Weather Intelligence
Platform and the Airflow code.

The image contains:

    /opt/airflow/dags
    /opt/airflow/orchestration
    /opt/airflow/w1
    /opt/airflow/w2
    /opt/airflow/w3
    /opt/airflow/w4
    /opt/airflow/w5
    /opt/airflow/w6
    /opt/airflow/w7
    /opt/airflow/w8
    /opt/airflow/w9

W10 is intentionally NOT inside this image at this stage.

W10 remains a separate Kubernetes application.

Why?

Because W10 is the API/dashboard application. W1-W9 are currently the
pipeline that Airflow orchestrates.

The DAG and orchestration code expect the paths:

    /opt/airflow/w1
    ...
    /opt/airflow/w9

So the Kubernetes image preserves these paths.

--------------------------------------------------
4. TEST THE AIRFLOW IMAGE BEFORE KUBERNETES
--------------------------------------------------

After building the image, test that the important Python dependencies exist:

    docker run --rm airflow-custom:k8 \
      python -c "import pyspark, psycopg2, boto3, minio, pyarrow, sklearn; print('Airflow image dependencies OK')"

Expected:

    Airflow image dependencies OK

You can also check that the project files exist:

    docker run --rm airflow-custom:k8 \
      bash -c "ls -ld /opt/airflow/dags /opt/airflow/orchestration /opt/airflow/w1 /opt/airflow/w2 /opt/airflow/w3 /opt/airflow/w4 /opt/airflow/w5 /opt/airflow/w6 /opt/airflow/w7 /opt/airflow/w8 /opt/airflow/w9"

Then test that Airflow can discover the DAG:

    docker run --rm \
      --env-file .env \
      -e POSTGRES_HOST=host.docker.internal \
      -e AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="postgresql+psycopg2://airflow:airflow@host.docker.internal:5432/airflow" \
      airflow-custom:k8 \
      airflow dags list

Expected DAG:

    weather_etl_pipeline

--------------------------------------------------
5. AIRFLOW INITIALIZATION
--------------------------------------------------

File:

    k8/airflow/airflow-init.yaml

This replaces the Docker Compose `airflow-init` service.

The Job prepares the Airflow database before the other Airflow services
start.

It does two important things:

1. Runs:

       airflow db migrate

2. Creates the Airflow admin user.

It uses:

    airflow-custom:k8

and the existing:

    weather-env

Secret.

It connects to Kubernetes PostgreSQL using the Kubernetes Service name:

    postgres:5432

This is different from using `localhost`.

Inside Kubernetes, services communicate using their Kubernetes Service names.

Deploy:

    kubectl apply -f k8/airflow/airflow-init.yaml

Check:

    kubectl get jobs
    kubectl get pods -l app=airflow-init

Logs:

    kubectl logs job/airflow-init

Expected successful result:

    airflow-init   Complete   1/1

Important:

This is a Job, not a Deployment.

It runs once and finishes.

If you change the Job YAML and need to run it again:

    kubectl delete job airflow-init

Then:

    kubectl apply -f k8/airflow/airflow-init.yaml

--------------------------------------------------
6. AIRFLOW API SERVER
--------------------------------------------------

File:

    k8/airflow/api-server.yaml

The API Server provides the Airflow web interface/API.

It replaces the Docker Compose:

    airflow-apiserver

Deploy only after `airflow-init` has completed.

    kubectl apply -f k8/airflow/api-server.yaml

Check:

    kubectl get deployment airflow-apiserver
    kubectl get pods -l app=airflow-apiserver
    kubectl get svc airflow-apiserver

Expected:

    READY  1/1

Check logs:

    kubectl logs deployment/airflow-apiserver

For local access:

    kubectl port-forward svc/airflow-apiserver 8080:8080

Then open:

    http://localhost:8080

The API Server uses the same:

    airflow-custom:k8

image and environment configuration as the original Docker Compose setup.

--------------------------------------------------
7. AIRFLOW SCHEDULER
--------------------------------------------------

File:

    k8/airflow/scheduler.yaml

The Scheduler is responsible for deciding when DAG tasks should run.

It replaces the Docker Compose:

    airflow-scheduler

It uses:

    LocalExecutor

This is intentional because the existing Docker Compose Airflow setup also
uses LocalExecutor.

Prerequisites:

- airflow-init must be Complete.
- PostgreSQL must be running.
- airflow-custom:k8 must exist.
- Airflow API Server can be running.

Deploy:

    kubectl apply -f k8/airflow/scheduler.yaml

Check:

    kubectl get deployment airflow-scheduler
    kubectl get pods -l app=airflow-scheduler

Expected:

    READY  1/1
    STATUS Running

Logs:

    kubectl logs deployment/airflow-scheduler

A healthy scheduler log should contain messages similar to:

    Loaded executor: :LocalExecutor:
    Starting the scheduler
    Worker starting up

The Scheduler is important because this is where Airflow starts executing
the tasks defined in the DAG.

--------------------------------------------------
8. AIRFLOW DAG PROCESSOR
--------------------------------------------------

File:

    k8/airflow/dag-processor.yaml

The DAG Processor reads the DAG files and processes their definitions.

It replaces the Docker Compose:

    airflow-dag-processor

It uses the same:

    airflow-custom:k8

image.

The image contains:

    /opt/airflow/dags
    /opt/airflow/orchestration
    /opt/airflow/w1 ... /opt/airflow/w9

Deploy:

    kubectl apply -f k8/airflow/dag-processor.yaml

Check:

    kubectl get deployment airflow-dag-processor
    kubectl get pods -l app=airflow-dag-processor

Expected:

    READY  1/1
    STATUS Running

Logs:

    kubectl logs deployment/airflow-dag-processor

A healthy DAG Processor should show that it found the DAG file, for example:

    Found 1 files for bundle dags-folder

and should register:

    weather_etl_pipeline

The DAG Processor reads/processes the DAG.

The Scheduler is still responsible for scheduling and executing the tasks.

--------------------------------------------------
9. HOW THE AIRFLOW PIECES WORK TOGETHER
--------------------------------------------------

It is easier to understand Kubernetes Airflow if you think of the components
as having different jobs.

AIRFLOW INIT:

    Prepare the Airflow database.

DAG PROCESSOR:

    Read the DAG file and register it with Airflow.

API SERVER:

    Give you the Airflow UI/API.

SCHEDULER:

    Decide when tasks should run and submit them to LocalExecutor.

LOCAL EXECUTOR:

    Execute the actual pipeline tasks.

So:

    airflow-init
         |
         v
    PostgreSQL
         |
         +-----------------------------+
         |                             |
         v                             v
    DAG Processor                 API Server
         |                             |
         v                             |
    weather_etl_pipeline               |
         |                             |
         +--------------+--------------+
                        |
                        v
                   Scheduler
                        |
                        v
                  LocalExecutor
                        |
                        v
                    W1 -> W9
                        |
                        v
                    AWS S3

--------------------------------------------------
10. HOW W1-W9 RUN
--------------------------------------------------

W1-W9 are not separate Kubernetes Deployments.

The DAG controls their order.

The current DAG flow is:

    create PostgreSQL table
             |
             v
    check pipeline state
             |
       +-----+-----+----------------+
       |           |                |
       v           v                v
    W1-W3       W3 only          Skip recovery
       |           |                |
       +-----------+----------------+
                   |
                   v
                  W4
                   |
                   v
                  W5
                   |
                   v
                  W6
                   |
                   v
                  W7
                   |
                   v
                  W8
                   |
                   v
                  W9
                   |
                   v
           Upload prediction to MinIO
                   |
                   v
             Upload artifacts
                   |
                   v
                 AWS S3
                   |
                   v
              End pipeline

The exact recovery decision is handled by:

    orchestration/check_archive.py

The database setup is handled by:

    orchestration/create_db.py

The AWS upload is handled by:

    orchestration/cloud_storage.py

These orchestration files are inside the Airflow image.

--------------------------------------------------
11. WHY POSTGRES IS `postgres:5432`
--------------------------------------------------

In Docker Compose, services used names such as:

    postgres
    weather-minio
    airflow-apiserver

Kubernetes works similarly.

The Kubernetes Services provide stable names.

Therefore:

    PostgreSQL = postgres:5432

    MinIO = weather-minio:9000

    Airflow API Server = airflow-apiserver:8080

Do not change these to `localhost` inside Kubernetes.

`localhost` means the current container/pod.

For example, from an Airflow pod:

    localhost:5432

would mean PostgreSQL inside that same Airflow pod, which is not what we want.

--------------------------------------------------
12. HOW TO CHECK EVERYTHING
--------------------------------------------------

Check all pods:

    kubectl get pods

Expected important pods:

    postgres-0
    weather-minio-0
    airflow-apiserver-...
    airflow-scheduler-...
    airflow-dag-processor-...
    airflow-init-...       Completed

Check Deployments:

    kubectl get deployment

Expected:

    airflow-apiserver
    airflow-scheduler
    airflow-dag-processor

Check Services:

    kubectl get svc

Expected important Services:

    postgres
    weather-minio
    airflow-apiserver

--------------------------------------------------
13. HOW TO OPEN AIRFLOW
--------------------------------------------------

Start:

    kubectl port-forward svc/airflow-apiserver 8080:8080

Then open:

    http://localhost:8080

The terminal will show:

    Forwarding from 127.0.0.1:8080 -> 8080

Keep this terminal running while using the UI.

Stop it with:

    Ctrl+C

--------------------------------------------------
14. HOW TO RUN THE PIPELINE
--------------------------------------------------

First make sure all Airflow components are healthy.

    kubectl get pods

Then open Airflow:

    kubectl port-forward svc/airflow-apiserver 8080:8080

Open:

    http://localhost:8080

Find:

    weather_etl_pipeline

From the Airflow UI, trigger the DAG.

Airflow should then execute the pipeline using the Kubernetes-hosted Airflow
environment.

The important thing to remember:

Kubernetes is running Airflow.

Airflow is orchestrating W1-W9.

The DAG decides the order.

The Python project code performs the actual work.

--------------------------------------------------
15. WHAT A SUCCESSFUL PIPELINE LOOKS LIKE
--------------------------------------------------

A successful run should show the DAG progressing through the tasks.

The pipeline should eventually reach:

    W1
    W2
    W3
    W4
    W5
    W6
    W7
    W8
    W9
    upload_prediction_to_minio
    upload_artifacts_to_s3
    end_pipeline

Depending on the archive/database state, W1-W3 may be skipped or recovery
tasks may run.

The important final result is that the DAG finishes successfully.

--------------------------------------------------
16. CURRENT VALIDATION RESULT
--------------------------------------------------

The local Kubernetes migration has been successfully tested.

Verified:

- PostgreSQL is running in Kubernetes.
- PostgreSQL storage is persistent through a PVC.
- MinIO is running in Kubernetes.
- MinIO storage is persistent through a PVC.
- `weather-env` Secret exists.
- `airflow-custom:k8` was successfully built.
- Airflow dependencies were tested inside the image.
- W1-W9 exist inside the Airflow image.
- The DAG was discovered successfully.
- Airflow initialization completed successfully.
- Airflow API Server is running.
- Airflow Scheduler is running.
- Airflow DAG Processor is running.
- Airflow UI was accessed through port-forwarding.
- `weather_etl_pipeline` was triggered from the Kubernetes-hosted Airflow UI.
- The pipeline completed successfully.

This means the local Kubernetes migration is not just configured; the actual
Airflow pipeline has been executed successfully.

--------------------------------------------------
17. IF SOMETHING FAILS
--------------------------------------------------

First check the pods:

    kubectl get pods

Then check the relevant logs.

Airflow API Server:

    kubectl logs deployment/airflow-apiserver

Scheduler:

    kubectl logs deployment/airflow-scheduler

DAG Processor:

    kubectl logs deployment/airflow-dag-processor

Airflow initialization:

    kubectl logs job/airflow-init

PostgreSQL:

    kubectl logs postgres-0

MinIO:

    kubectl logs weather-minio-0

For a pod that is not starting:

    kubectl describe pod <pod-name>

For a Deployment:

    kubectl describe deployment <deployment-name>

--------------------------------------------------
18. IMPORTANT RULE FOR FUTURE CHANGES
--------------------------------------------------

If you change the Python code used by W1-W9, orchestration, or the DAG and
that code is copied into the Airflow Docker image, rebuild the image:

    docker build -f k8/airflow/Dockerfile -t airflow-custom:k8 .

Then restart/redeploy the affected Airflow components if necessary.

If only a Kubernetes YAML file changes, you normally only need to apply the
changed YAML:

    kubectl apply -f <file>.yaml

If a Job such as `airflow-init` needs to run again, delete the old Job first:

    kubectl delete job airflow-init

Then apply it again.

--------------------------------------------------
19. SIMPLE WAY TO REMEMBER THE WHOLE SYSTEM
--------------------------------------------------

Think about it like this:

    PostgreSQL
        =
    Airflow's database

    MinIO
        =
    Object storage used by the platform

    Airflow API Server
        =
    Airflow website/API

    DAG Processor
        =
    Reads the DAG

    Scheduler
        =
    Decides what should run

    LocalExecutor
        =
    Actually runs the tasks

    W1-W9
        =
    The pipeline work

    orchestration/
        =
    Extra control logic around the pipeline

    AWS S3
        =
    Cloud destination for selected artifacts

    W10
        =
    Separate API + dashboard application

--------------------------------------------------
20. NEXT STAGE
--------------------------------------------------

The local Kubernetes migration has now been validated.

The next stage is not to redesign W1-W9.

The next stage is to take this working Kubernetes project and prepare it
for deployment to the Oracle Cloud VM using K3s.

The intended flow is:

    Local Kubernetes
          |
          v
       Git push
          |
          v
    Oracle Cloud VM
          |
          v
          K3s
          |
          v
    Kubernetes manifests
          |
          v
    Weather Intelligence Platform

AWS remains the external cloud storage source/destination where the project
already uses it.

W10 can remain a separate Kubernetes application until the next planned
integration step.
