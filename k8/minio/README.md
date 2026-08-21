# MinIO Kubernetes deployment

Uses the existing `weather-env` Secret.

Required Secret keys:
- MINIO_ACCESS_KEY
- MINIO_SECRET_KEY

For in-cluster clients:
- MINIO_ENDPOINT=weather-minio:9000
- MINIO_SECURE=False

Deploy:
kubectl apply -f k8/minio/pvc.yaml
kubectl apply -f k8/minio/statefulset.yaml
kubectl apply -f k8/minio/service.yaml

Verify:
kubectl get pods -l app=weather-minio
kubectl get svc weather-minio
kubectl get pvc minio-data

Readiness:
kubectl exec -it weather-minio-0 -- curl -f http://localhost:9000/minio/health/ready

Console:
kubectl port-forward svc/weather-minio 9001:9001
Open http://localhost:9001
