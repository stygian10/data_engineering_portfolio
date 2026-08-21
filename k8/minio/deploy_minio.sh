#!/bin/bash
set -e
kubectl get secret weather-env >/dev/null
kubectl apply -f k8/minio/pvc.yaml
kubectl apply -f k8/minio/statefulset.yaml
kubectl apply -f k8/minio/service.yaml
kubectl rollout status statefulset/weather-minio --timeout=180s
kubectl get pods -l app=weather-minio
kubectl get svc weather-minio
kubectl get pvc minio-data
