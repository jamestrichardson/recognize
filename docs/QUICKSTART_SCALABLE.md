# Quick Start: Scalable Architecture

## Prerequisites

- Docker and Docker Compose installed
- Model files in `models/` directory
- At least 8GB RAM available

## Option 1: Simple Setup (Original)

Run without task queue (synchronous processing):

```bash
docker-compose up --build
```

Access at: <http://localhost:5000>

## Option 2: Scalable Setup (Recommended)

Run with task queue and separate worker containers:

```bash
# Start all services with 2 workers each
docker-compose -f docker-compose.scalable.yml up --build

# Or scale workers as needed
docker-compose -f docker-compose.scalable.yml up --build \
  --scale face-worker=3 \
  --scale object-worker=3
```

Access:

- Web UI: <http://localhost:5000>
- Monitoring (Flower): <http://localhost:5555>
- Redis: localhost:6379

## Services Running

| Service | Purpose | Scaling |
|---------|---------|---------|
| web | Flask API | Fixed (1) |
| redis | Message broker | Fixed (1) |
| face-worker | Face detection | ✅ Scalable |
| object-worker | Object detection | ✅ Scalable |
| flower | Monitoring | Optional |

## Testing Async API

### 1. Upload and Queue Task

```bash
curl -X POST http://localhost:5000/api/detect/face/image \
  -F "file=@/path/to/image.jpg"
```

Response:

```json
{
  "success": true,
  "data": {
    "task_id": "abc-123-def-456",
    "status": "queued"
  }
}
```

### 2. Check Task Status

```bash
curl http://localhost:5000/api/task/abc-123-def-456

While processing:

```json
{
  "success": true,
  "data": {
    "state": "PROCESSING",
    "status": "Detecting faces in image"
  }
}
```

When complete:

```json
{
  "success": true,
  "data": {
    "state": "SUCCESS",
    "result": { ... full results ... }
  }
}
```
```text

## Monitoring
```

```text


View:

- Active/completed tasks
- Worker status
- Queue sizes
- Task execution times

## Scaling Workers

### During Runtime

```bash
# Scale up face workers to 5
docker-compose -f docker-compose.scalable.yml up --scale face-worker=5 -d

# Scale down object workers to 1
docker-compose -f docker-compose.scalable.yml up --scale object-worker=1 -d


### In Configuration

Edit `docker-compose.scalable.yml`:

```yaml
face-worker:
  deploy:
    replicas: 5  # Change this number


## Environment Variables

Copy and configure:

```bash
cp .env.example .env
```text

Key settings for scalable mode:

```bash
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0


## Common Issues

### Workers not processing

```bash
# Check Redis
docker-compose logs redis

# Check worker logs
docker-compose logs face-worker
docker-compose logs object-worker


### Out of memory

Reduce worker concurrency in Dockerfiles:

```dockerfile
CMD ["celery", "-A", "app.celery_app", "worker", \
     "--concurrency=1", \  # Lower this
     ...]


## Development Mode

For local development without Docker:

1. Start Redis:

```bash
docker run -p 6379:6379 redis:7-alpine


1. Start Flask app:

```bash
python run.py


1. Start face worker:

```bash
celery -A app.celery_app worker --queues=face_detection --loglevel=info


1. Start object worker:

```bash
celery -A app.celery_app worker --queues=object_detection --loglevel=info


## Next Steps

See [docs/SCALABLE_ARCHITECTURE.md](docs/SCALABLE_ARCHITECTURE.md) for:

- Detailed architecture explanation
- Production deployment guide
- Performance tuning
- Kubernetes deployment
- Monitoring and troubleshooting
