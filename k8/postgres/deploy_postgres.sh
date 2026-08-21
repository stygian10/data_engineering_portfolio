#!/bin/bash
set -e

kubectl get secret weather-env >/dev/null

kubectl apply -f k8/postgres/pvc.yaml
kubectl apply -f k8/postgres/statefulset.yaml
kubectl apply -f k8/postgres/service.yaml

kubectl rollout status statefulset/postgres --timeout=180s
kubectl get pods -l app=postgres
kubectl get svc postgres
kubectl get pvc postgres-data
