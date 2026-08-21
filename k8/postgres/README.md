# PostgreSQL Kubernetes deployment

This deployment preserves the existing PostgreSQL 16 Compose service while moving it to local Kubernetes.

## Important

`weather-env` is expected to already exist in the cluster.

The existing project uses these variables:

- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB
- POSTGRES_PORT

The Kubernetes Service is named `postgres`, so workloads inside the cluster should use:

POSTGRES_HOST=postgres

## Deploy

kubectl apply -f k8/postgres/pvc.yaml
kubectl apply -f k8/postgres/statefulset.yaml
kubectl apply -f k8/postgres/service.yaml

## Verify

kubectl get pvc
kubectl get pods -l app=postgres
kubectl get svc postgres

## Connection test

kubectl exec -it postgres-0 -- pg_isready -U airflow -d airflow

Do not delete the PVC unless you intentionally want to delete PostgreSQL data.
