# Recognize Helm Chart

This Helm chart deploys the Recognize application (facial and object recognition) on Kubernetes with a scalable architecture.

## Architecture

The chart deploys:

- **Web Application**: Flask web server (default: 2 replicas)
- **Face Detection Worker**: Celery worker for face detection tasks (default: 2 replicas)
- **Object Detection Worker**: Celery worker for object detection tasks (default: 2 replicas)
- **Redis**: Task queue broker and result backend (optional, enabled by default)
- **Flower**: Celery monitoring UI (optional, disabled by default)

## Prerequisites

- Kubernetes 1.19+
- Helm 3.8+
- PV provisioner support in the underlying infrastructure (for persistent storage)
- Ingress controller (optional, for external access)

## Installation

### From OCI Registry (Recommended)

```bash
# Add the Helm repository
helm registry login ghcr.io -u <your-github-username>

# Install the chart
helm install recognize oci://ghcr.io/jamestrichardson/helm/recognize \
  --namespace recognize \
  --create-namespace

# Or with custom values
helm install recognize oci://ghcr.io/jamestrichardson/helm/recognize \
  --namespace recognize \
  --create-namespace \
  --values custom-values.yaml
```

### From Source

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

The following table lists the configurable parameters of the Recognize chart and their default values.

### Application Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount.web` | Number of web application replicas | `2` |
| `replicaCount.faceWorker` | Number of face detection worker replicas | `2` |
| `replicaCount.objectWorker` | Number of object detection worker replicas | `2` |
| `image.repository` | Image repository | `teknofile/recognize` |
| `image.tag` | Image tag (overrides Chart appVersion) | `"1.1.0"` |
| `image.pullPolicy` | Image pull policy | `IfNotPresent` |

### Service Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `service.type` | Kubernetes service type | `ClusterIP` |
| `service.port` | Service port | `5000` |

### Ingress Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ingress.enabled` | Enable ingress controller | `false` |
| `ingress.className` | Ingress class name | `nginx` |
| `ingress.host` | Hostname for the application | `recognize.example.com` |
| `ingress.annotations` | Ingress annotations | `{}` |
| `ingress.tls` | TLS configuration | `[]` |

### Resource Limits

| Parameter | Description | Default |
|-----------|-------------|---------|
| `resources.web.requests.cpu` | Web CPU request | `500m` |
| `resources.web.requests.memory` | Web memory request | `512Mi` |
| `resources.faceWorker.requests.cpu` | Face worker CPU request | `1000m` |
| `resources.faceWorker.requests.memory` | Face worker memory request | `1Gi` |
| `resources.faceWorker.limits.cpu` | Face worker CPU limit | `2000m` |
| `resources.faceWorker.limits.memory` | Face worker memory limit | `2Gi` |

### Autoscaling

| Parameter | Description | Default |
|-----------|-------------|---------|
| `autoscaling.web.enabled` | Enable HPA for web | `false` |
| `autoscaling.web.minReplicas` | Minimum replicas | `2` |
| `autoscaling.web.maxReplicas` | Maximum replicas | `10` |
| `autoscaling.web.targetCPUUtilizationPercentage` | Target CPU % | `80` |

### Persistence

| Parameter | Description | Default |
|-----------|-------------|---------|
| `persistence.uploads.enabled` | Enable uploads PVC | `true` |
| `persistence.uploads.size` | Uploads PVC size | `10Gi` |
| `persistence.uploads.accessMode` | Uploads access mode | `ReadWriteMany` |
| `persistence.models.enabled` | Enable models PVC | `true` |
| `persistence.models.size` | Models PVC size | `5Gi` |
| `persistence.models.accessMode` | Models access mode | `ReadOnlyMany` |

### Redis

| Parameter | Description | Default |
|-----------|-------------|---------|
| `redis.enabled` | Deploy Redis instance | `true` |
| `redis.auth.enabled` | Enable Redis authentication | `false` |
| `redis.master.persistence.enabled` | Enable Redis persistence | `true` |
| `redis.master.persistence.size` | Redis PVC size | `8Gi` |

### Monitoring

| Parameter | Description | Default |
|-----------|-------------|---------|
| `monitoring.flower.enabled` | Enable Flower monitoring | `false` |
| `monitoring.flower.ingress.enabled` | Enable Flower ingress | `false` |
| `monitoring.flower.ingress.host` | Flower hostname | `flower.recognize.example.com` |

## Examples

### Production Deployment with Ingress and TLS

```yaml
# production-values.yaml
replicaCount:
  web: 3
  faceWorker: 4
  objectWorker: 4

image:
  tag: "1.1.0"

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

autoscaling:
  web:
    enabled: true
    minReplicas: 3
    maxReplicas: 20
    targetCPUUtilizationPercentage: 70
  faceWorker:
    enabled: true
    minReplicas: 4
    maxReplicas: 30
  objectWorker:
    enabled: true
    minReplicas: 4
    maxReplicas: 30

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
      username: admin
      password: "changeme"

redis:
  auth:
    enabled: true
    password: "secure-redis-password"
  master:
    persistence:
      enabled: true
      size: 20Gi
```

### Development Deployment with External Redis

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

redis:
  enabled: false

celery:
  brokerUrl: "redis://external-redis.example.com:6379/0"
  resultBackend: "redis://external-redis.example.com:6379/0"
```

## Upgrading

```bash
# Upgrade to latest version from OCI registry
helm upgrade recognize oci://ghcr.io/jamestrichardson/helm/recognize \
  --namespace recognize

# Upgrade with custom values
helm upgrade recognize oci://ghcr.io/jamestrichardson/helm/recognize \
  --namespace recognize \
  --values production-values.yaml
```

## Uninstalling

```bash
# Uninstall the release
helm uninstall recognize --namespace recognize

# Delete PVCs (if needed)
kubectl delete pvc -n recognize -l app.kubernetes.io/instance=recognize
```

## Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods -n recognize

# Check pod events
kubectl describe pod -n recognize <pod-name>

# View pod logs
kubectl logs -n recognize <pod-name>
```

### Redis Connection Issues

```bash
# Check Redis pod status
kubectl get pods -n recognize -l app.kubernetes.io/component=redis

# Test Redis connection from web pod
kubectl exec -n recognize -it deployment/recognize-web -- \
  sh -c 'python -c "import redis; r = redis.from_url(\"$CELERY_BROKER_URL\"); print(r.ping())"'
```

### Storage Issues

```bash
# Check PVC status
kubectl get pvc -n recognize

# Check PV status
kubectl get pv | grep recognize

# Describe PVC for events
kubectl describe pvc -n recognize recognize-uploads
```

## Version Management

This Helm chart version and the application version are automatically managed by release-please:

- **Chart Version** (`version`): Follows the application semantic version
- **App Version** (`appVersion`): Matches the Docker image tag released
- **Image Tag** (`image.tag`): Set to the released version

When a new release is created, release-please will:

1. Update the version in `Chart.yaml`
2. Update the appVersion in `Chart.yaml`
3. Update the default image tag in `values.yaml`
4. Package and publish the chart to `ghcr.io/jamestrichardson/helm/recognize`

## Support

For issues, questions, or contributions, please visit:

- GitHub: <https://github.com/jamestrichardson/recognize>
- Issues: <https://github.com/jamestrichardson/recognize/issues>
