# Scalable Architecture Guide

## Overview

This document describes the scalable architecture for the Recognize application, which separates compute-intensive facial recognition and object detection tasks into independent worker containers.

## Architecture Components

### 1. **Flask Web Application** (`web` service)

- Handles HTTP requests
- Accepts file uploads
- Queues tasks to workers
- Returns task IDs for async operations
- Serves results

### 2. **Redis** (`redis` service)

- Message broker for Celery
- Stores task results
- Manages task queues

### 3. **Face Detection Workers** (`face-worker` service)

- Dedicated workers for facial recognition
- Process tasks from `face_detection` queue
- Can be scaled independently
- Resource limits: 1 CPU, 2GB RAM per worker

### 4. **Object Detection Workers** (`object-worker` service)

- Dedicated workers for object detection
- Process tasks from `object_detection` queue
- Can be scaled independently
- Resource limits: 2 CPU, 4GB RAM per worker (YOLO is more resource-intensive)

### 5. **Flower** (`flower` service) - Optional

- Real-time monitoring dashboard
- View task status, worker status, and queue sizes
- Accessible at <http://localhost:5555>

## Architecture Diagram

```text
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTP Request
       ▼
┌─────────────────────────────────┐
│   Flask Web App (web)           │
│  - Accept uploads               │
│  - Queue tasks to Redis         │
│  - Return task_id               │
└────────┬────────────────────────┘
         │ Enqueue Task
         ▼
┌─────────────────────────────────┐
│   Redis (Message Broker)        │
│  - face_detection queue         │
│  - object_detection queue       │
└────┬────────────────────────┬───┘
     │                        │
     │                        │
     ▼                        ▼
┌──────────────────┐  ┌──────────────────┐
│ Face Workers     │  │ Object Workers   │
│ (scalable)       │  │ (scalable)       │
│ - Worker 1       │  │ - Worker 1       │
│ - Worker 2       │  │ - Worker 2       │
│ - Worker N...    │  │ - Worker N...    │
└──────────────────┘  └──────────────────┘
```text

## How It Works

### Synchronous Flow (Without Celery)

1. Client uploads file
2. Web app processes immediately
3. Client waits for response
4. Response contains results

### Asynchronous Flow (With Celery)

1. Client uploads file
2. Web app saves file and queues task
3. Web app immediately returns task_id (202 Accepted)
4. Worker picks up task from queue
5. Worker processes file
6. Worker stores result in Redis
7. Client polls `/api/task/<task_id>` to check status
8. When complete, client retrieves results

## API Changes

### Async Endpoints

All detection endpoints now return immediately with a task ID:

```bash
POST /api/detect/face/image
Response (202 Accepted):
{
  "success": true,
  "data": {
    "task_id": "abc-123-def-456",
    "status": "queued",
    "message": "Face detection task queued. Use task_id to check status."
  }
}
```text

### Check Task Status

```bash
GET /api/task/{task_id}

Response (Processing):
{
  "success": true,
  "data": {
    "state": "PROCESSING",
    "status": "Detecting faces in image"
  }
}

Response (Complete):
{
  "success": true,
  "data": {
    "state": "SUCCESS",
    "result": {
      "success": true,
      "faces_detected": 3,
      "faces": [...],
      "annotated_image": "..."
    }
  }
}
```text

## Deployment

### Development (Local)

Run with standard Docker Compose:

```bash
docker-compose -f docker-compose.scalable.yml up --build
```text

### Production Deployment

#### 1. Basic Scaling (Docker Compose)

Scale workers independently:

```bash
# Scale face detection workers to 5
docker-compose -f docker-compose.scalable.yml up --scale face-worker=5 --scale object-worker=3

# Or modify docker-compose.scalable.yml:
# face-worker:
#   deploy:
#     replicas: 5
```text

#### 2. Advanced Scaling (Kubernetes)

For Kubernetes deployment:

- Convert Docker Compose to K8s manifests
- Use Horizontal Pod Autoscaler (HPA) for auto-scaling
- Configure based on CPU/Memory or queue length

Example HPA configuration:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: face-worker-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: face-worker
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```text

#### 3. Cloud-Managed Services

Replace components with cloud services:

- **Redis**: AWS ElastiCache, Azure Cache for Redis, GCP Memorystore
- **Workers**: AWS ECS/Fargate, Azure Container Instances, GCP Cloud Run
- **Message Queue**: AWS SQS, Azure Service Bus (requires adapter)

## Monitoring

### Flower Dashboard

Access at <http://localhost:5555>

- View active/completed tasks
- Monitor worker health
- See queue lengths
- Task execution time metrics

### Metrics to Monitor

1. **Queue Length**: Indicates if more workers needed
2. **Task Success Rate**: Detect failing tasks
3. **Worker CPU/Memory**: Optimize resource allocation
4. **Task Processing Time**: Identify bottlenecks

### Logging

All workers log to mounted volumes:

```text
./logs/
├── face_worker_1.log
├── face_worker_2.log
├── object_worker_1.log
└── object_worker_2.log
```text

## Performance Tuning

### Worker Concurrency

Adjust in Dockerfile or docker-compose:

```bash
# Low concurrency for memory-intensive tasks
--concurrency=2

# Higher for lighter tasks
--concurrency=4
```text

### Resource Limits

Set in docker-compose.scalable.yml:

```yaml
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 4G
    reservations:
      cpus: '1.0'
      memory: 2G
```text

### Task Prefetching

Configure in `app/celery_app.py`:

```python
worker_prefetch_multiplier=1  # One task at a time
# or
worker_prefetch_multiplier=4  # 4 tasks per worker
```text

## Scaling Strategies

### Vertical Scaling

- Increase CPU/Memory per worker
- Better for complex models (YOLO)
- Limited by single machine resources

### Horizontal Scaling

- Add more worker containers
- Better for high request volume
- Unlimited scaling potential

### Auto-Scaling Rules

```text
IF queue_length > 100 AND avg_wait_time > 30s:
    scale_workers += 2

IF queue_length < 10 AND cpu_usage < 30%:
    scale_workers -= 1 (min: 1)
```text

## Cost Optimization

### Strategies

1. **Use spot/preemptible instances** for workers (can handle interruptions)
2. **Scale down during off-hours** (scheduled scaling)
3. **Use CPU-only instances** for Haar Cascade face detection
4. **Use GPU instances** only for deep learning models (optional)
5. **Implement task result expiration** (auto-cleanup)

### Example Auto-scaling Schedule

```text
Monday-Friday 9am-5pm: 10 workers
Monday-Friday 5pm-9am: 2 workers
Weekends: 1 worker
```text

## Troubleshooting

### Workers Not Processing Tasks

1. Check Redis connection: `docker-compose logs redis`
2. Verify worker logs: `docker-compose logs face-worker`
3. Ensure queues are configured: Check `app/celery_app.py`

### High Memory Usage

1. Reduce worker concurrency
2. Enable `worker_max_tasks_per_child` to restart workers periodically
3. Implement file cleanup after processing

### Slow Processing

1. Increase `frame_skip` for videos
2. Add more workers
3. Reduce image resolution before processing
4. Use GPU-accelerated OpenCV

## Migration Path

### Phase 1: Development/Testing

- Use provided docker-compose.scalable.yml
- Test with 2 workers per type

### Phase 2: Small Production

- Deploy to cloud VM
- Scale to 5-10 workers per type
- Monitor with Flower

### Phase 3: Large Scale

- Migrate to Kubernetes
- Implement auto-scaling
- Use managed Redis service
- Add load balancer for web instances

## Security Considerations

1. **Network Isolation**: Use Docker networks to isolate Redis
2. **Redis Authentication**: Set password in production
3. **Result Encryption**: Encrypt sensitive detection results
4. **Task Timeouts**: Prevent runaway tasks
5. **File Cleanup**: Auto-delete processed files

## Alternatives to Celery

If Celery doesn't fit your needs:

### 1. **RabbitMQ + Pika**

- More robust message broker
- Better for complex routing

### 2. **AWS SQS + Lambda**

- Fully managed
- Pay per execution
- No infrastructure management

### 3. **Apache Kafka**

- Better for high-throughput streaming
- More complex setup

### 4. **Redis Queue (RQ)**

- Simpler than Celery
- Python-native
- Fewer features

## Conclusion

This scalable architecture allows you to:

- ✅ Handle high request volumes
- ✅ Scale face and object detection independently
- ✅ Optimize resource allocation
- ✅ Provide responsive API (immediate task_id response)
- ✅ Monitor and debug easily
- ✅ Deploy to any cloud platform

Start with the basic setup and scale as your traffic grows!
