# Helm Chart Installation Guide

This guide provides detailed instructions for deploying the Recognize application to Kubernetes using Helm.

## Prerequisites

Before installing the Helm chart, ensure you have:

- Kubernetes cluster (version 1.19+)
- `kubectl` configured to access your cluster
- Helm 3.8 or later installed
- (Optional) Ingress controller (e.g., nginx-ingress, Traefik)
- (Optional) Storage provisioner for persistent volumes

## Quick Start

### Install from OCI Registry

```bash
# Install the chart
helm install recognize oci://ghcr.io/jamestrichardson/helm/recognize \
  --version 1.1.0 \
  --namespace recognize \
  --create-namespace

# Check deployment status
kubectl get pods -n recognize
```

### Install from Source

```bash
# Clone the repository
git clone https://github.com/jamestrichardson/recognize.git
cd recognize

# Install the chart
helm install recognize ./helm/recognize \
  --namespace recognize \
  --create-namespace
```

## Configuration

### Basic Configuration

Create a `values.yaml` file to customize your deployment:

```yaml
# values.yaml
replicaCount:
  web: 3
  faceWorker: 4
  objectWorker: 4

image:
  repository: teknofile/recognize
  tag: "1.1.0"
  pullPolicy: IfNotPresent

ingress:
  enabled: true
  className: nginx
  host: recognize.example.com
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
  tls:
    - secretName: recognize-tls
      hosts:
        - recognize.example.com

persistence:
  uploads:
    enabled: true
    size: 50Gi
    storageClass: "fast-ssd"
  models:
    enabled: true
    size: 10Gi
    storageClass: "standard"
```

Install with custom values:

```bash
helm install recognize oci://ghcr.io/jamestrichardson/helm/recognize \
  --namespace recognize \
  --create-namespace \
  --values values.yaml
```

### Using External Redis

If you have an existing Redis instance:

```yaml
# values.yaml
redis:
  enabled: false

celery:
  brokerUrl: "redis://my-redis.example.com:6379/0"
  resultBackend: "redis://my-redis.example.com:6379/0"
```

### Enable Autoscaling

```yaml
# values.yaml
autoscaling:
  web:
    enabled: true
    minReplicas: 2
    maxReplicas: 20
    targetCPUUtilizationPercentage: 70
  faceWorker:
    enabled: true
    minReplicas: 2
    maxReplicas: 30
    targetCPUUtilizationPercentage: 80
  objectWorker:
    enabled: true
    minReplicas: 2
    maxReplicas: 30
    targetCPUUtilizationPercentage: 80
```

### Enable Flower Monitoring

```yaml
# values.yaml
monitoring:
  flower:
    enabled: true
    ingress:
      enabled: true
      host: flower.recognize.example.com
      annotations:
        cert-manager.io/cluster-issuer: "letsencrypt-prod"
      tls:
        - secretName: flower-tls
          hosts:
            - flower.recognize.example.com
    auth:
      enabled: true
      username: "admin"
      password: "secure-password-here"
```

## Installation Examples

### Development Environment

Minimal setup for local testing:

```yaml
# dev-values.yaml
replicaCount:
  web: 1
  faceWorker: 1
  objectWorker: 1

image:
  tag: "latest"
  pullPolicy: Always

persistence:
  uploads:
    enabled: false
  models:
    enabled: false

resources:
  web:
    requests:
      cpu: 100m
      memory: 256Mi
  faceWorker:
    requests:
      cpu: 500m
      memory: 512Mi
  objectWorker:
    requests:
      cpu: 500m
      memory: 512Mi
```

```bash
helm install recognize ./helm/recognize \
  --namespace recognize-dev \
  --create-namespace \
  --values dev-values.yaml
```

### Production Environment

Full production setup with high availability:

```yaml
# prod-values.yaml
replicaCount:
  web: 5
  faceWorker: 10
  objectWorker: 10

image:
  repository: teknofile/recognize
  tag: "1.1.0"
  pullPolicy: IfNotPresent

resources:
  web:
    requests:
      cpu: 500m
      memory: 512Mi
    limits:
      cpu: 2000m
      memory: 2Gi
  faceWorker:
    requests:
      cpu: 1000m
      memory: 1Gi
    limits:
      cpu: 2000m
      memory: 2Gi
  objectWorker:
    requests:
      cpu: 1000m
      memory: 1Gi
    limits:
      cpu: 2000m
      memory: 2Gi

ingress:
  enabled: true
  className: nginx
  host: recognize.example.com
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/proxy-body-size: "100m"
  tls:
    - secretName: recognize-tls
      hosts:
        - recognize.example.com

persistence:
  uploads:
    enabled: true
    size: 100Gi
    storageClass: "fast-ssd"
    accessMode: ReadWriteMany
  models:
    enabled: true
    size: 20Gi
    storageClass: "standard"
    accessMode: ReadOnlyMany

autoscaling:
  web:
    enabled: true
    minReplicas: 5
    maxReplicas: 50
    targetCPUUtilizationPercentage: 70
    targetMemoryUtilizationPercentage: 80
  faceWorker:
    enabled: true
    minReplicas: 10
    maxReplicas: 100
    targetCPUUtilizationPercentage: 80
  objectWorker:
    enabled: true
    minReplicas: 10
    maxReplicas: 100
    targetCPUUtilizationPercentage: 80

redis:
  auth:
    enabled: true
    password: "super-secure-redis-password"
  master:
    persistence:
      enabled: true
      size: 50Gi
      storageClass: "fast-ssd"
    resources:
      requests:
        cpu: 500m
        memory: 512Mi
      limits:
        cpu: 2000m
        memory: 2Gi

monitoring:
  flower:
    enabled: true
    ingress:
      enabled: true
      host: flower.recognize.example.com
      annotations:
        cert-manager.io/cluster-issuer: "letsencrypt-prod"
      tls:
        - secretName: flower-tls
          hosts:
            - flower.recognize.example.com
    auth:
      enabled: true
      username: "admin"
      password: "secure-flower-password"

config:
  secretKey: "your-super-secure-secret-key-here"
  maxContentLength: "104857600"  # 100MB
  faceDetectionConfidence: "0.6"
  objectDetectionConfidence: "0.5"
```

```bash
helm install recognize oci://ghcr.io/jamestrichardson/helm/recognize \
  --version 1.1.0 \
  --namespace recognize \
  --create-namespace \
  --values prod-values.yaml
```

## Post-Installation

### Verify Installation

```bash
# Check all pods are running
kubectl get pods -n recognize

# Check services
kubectl get svc -n recognize

# Check ingress
kubectl get ingress -n recognize

# View logs
kubectl logs -n recognize -l app.kubernetes.io/component=web --tail=50
kubectl logs -n recognize -l app.kubernetes.io/component=face-worker --tail=50
kubectl logs -n recognize -l app.kubernetes.io/component=object-worker --tail=50
```

### Access the Application

#### Without Ingress (Port Forward)

```bash
# Forward web application port
kubectl port-forward -n recognize svc/recognize-web 5000:5000

# Access at: http://localhost:5000
```

#### With Ingress

Access the application at your configured hostname:

```bash
# Check ingress configuration
kubectl describe ingress -n recognize recognize-web

# Access at: https://recognize.example.com
```

### Monitor Celery Tasks (Flower)

```bash
# Port forward Flower
kubectl port-forward -n recognize svc/recognize-flower 5555:5555

# Access at: http://localhost:5555
```

## Upgrading

### Upgrade to New Version

```bash
# Upgrade from OCI registry
helm upgrade recognize oci://ghcr.io/jamestrichardson/helm/recognize \
  --version 1.2.0 \
  --namespace recognize \
  --values prod-values.yaml

# Or from source
helm upgrade recognize ./helm/recognize \
  --namespace recognize \
  --values prod-values.yaml
```

### Update Configuration Only

```bash
# Update values without changing version
helm upgrade recognize oci://ghcr.io/jamestrichardson/helm/recognize \
  --namespace recognize \
  --reuse-values \
  --set replicaCount.web=10
```

### Rollback

```bash
# List releases
helm history recognize -n recognize

# Rollback to previous version
helm rollback recognize -n recognize

# Rollback to specific revision
helm rollback recognize 2 -n recognize
```

## Scaling

### Manual Scaling

```bash
# Scale web application
kubectl scale deployment recognize-web -n recognize --replicas=10

# Scale workers
kubectl scale deployment recognize-face-worker -n recognize --replicas=20
kubectl scale deployment recognize-object-worker -n recognize --replicas=20
```

### Using Helm

```bash
helm upgrade recognize oci://ghcr.io/jamestrichardson/helm/recognize \
  --namespace recognize \
  --reuse-values \
  --set replicaCount.web=10 \
  --set replicaCount.faceWorker=20 \
  --set replicaCount.objectWorker=20
```

## Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods -n recognize

# Describe problematic pod
kubectl describe pod <pod-name> -n recognize

# Check events
kubectl get events -n recognize --sort-by='.lastTimestamp'
```

### Redis Connection Issues

```bash
# Check Redis pod
kubectl get pods -n recognize -l app.kubernetes.io/component=redis

# Test Redis connection from web pod
kubectl exec -n recognize -it deployment/recognize-web -- \
  sh -c 'python -c "import redis; r = redis.from_url(\"$CELERY_BROKER_URL\"); print(r.ping())"'

# Check Redis logs
kubectl logs -n recognize -l app.kubernetes.io/component=redis --tail=100
```

### Storage Issues

```bash
# Check PVC status
kubectl get pvc -n recognize

# Describe PVC
kubectl describe pvc recognize-uploads -n recognize
kubectl describe pvc recognize-models -n recognize

# Check PV status
kubectl get pv | grep recognize
```

### Image Pull Issues

```bash
# Check image pull secrets
kubectl get secrets -n recognize

# Describe pod to see image pull errors
kubectl describe pod <pod-name> -n recognize

# Verify image exists
docker pull teknofile/recognize:1.1.0
```

### Health Check Failures

```bash
# Check application health endpoint
kubectl exec -n recognize -it deployment/recognize-web -- \
  curl -v http://localhost:5000/api/health

# Check readiness/liveness probe configuration
kubectl describe pod <pod-name> -n recognize | grep -A 10 Liveness
```

## Uninstalling

### Remove Deployment

```bash
# Uninstall the release
helm uninstall recognize --namespace recognize

# Verify removal
kubectl get all -n recognize
```

### Clean Up Persistent Storage

**Warning:** This will delete all uploaded files and data!

```bash
# Delete PVCs
kubectl delete pvc -n recognize -l app.kubernetes.io/instance=recognize

# Delete namespace (removes everything)
kubectl delete namespace recognize
```

## Advanced Configuration

### Custom Secret Key

```bash
# Generate a secure secret key
SECRET_KEY=$(openssl rand -hex 32)

# Install with custom secret
helm install recognize oci://ghcr.io/jamestrichardson/helm/recognize \
  --namespace recognize \
  --create-namespace \
  --set config.secretKey="$SECRET_KEY"
```

### Using Existing Secrets

```bash
# Create secret manually
kubectl create secret generic recognize-secret \
  --from-literal=SECRET_KEY=your-secret-key \
  --namespace recognize

# Disable secret creation in values
helm install recognize oci://ghcr.io/jamestrichardson/helm/recognize \
  --namespace recognize \
  --create-namespace \
  --set existingSecret=recognize-secret
```

### Resource Quotas

Ensure your namespace has sufficient quotas:

```bash
# Check namespace quotas
kubectl describe quota -n recognize

# Check resource usage
kubectl top pods -n recognize
kubectl top nodes
```

## Performance Tuning

### Worker Concurrency

Adjust Celery worker concurrency for your workload:

```yaml
# values.yaml
celery:
  faceWorker:
    concurrency: 4
  objectWorker:
    concurrency: 4
```

### Resource Allocation

Fine-tune resource requests/limits based on monitoring:

```yaml
resources:
  faceWorker:
    requests:
      cpu: 2000m      # 2 CPU cores
      memory: 2Gi
    limits:
      cpu: 4000m      # 4 CPU cores max
      memory: 4Gi
```

### Redis Persistence

For better performance, consider using a managed Redis service:

```yaml
redis:
  enabled: false

celery:
  brokerUrl: "redis://my-elasticache.amazonaws.com:6379/0"
  resultBackend: "redis://my-elasticache.amazonaws.com:6379/0"
```

## Security Best Practices

1. **Always use TLS/SSL for ingress**
2. **Enable Redis authentication in production**
3. **Use strong secret keys**
4. **Run containers as non-root user** (enabled by default)
5. **Keep the chart and images updated**
6. **Use network policies to restrict pod communication**
7. **Enable Pod Security Standards**

## Support

For issues or questions:

- **Documentation**: [README.md](../README.md)
- **GitHub Issues**: <https://github.com/jamestrichardson/recognize/issues>
- **Helm Chart**: <https://github.com/jamestrichardson/recognize/tree/main/helm/recognize>

## Version History

- **1.1.0** - Initial Helm chart release with full Kubernetes support
- Includes web app, face/object workers, Redis, and optional Flower monitoring
- Supports autoscaling, persistence, and production-ready configurations
