#!/usr/bin/env bash
# Start Celery object detection worker

echo "Starting Object Detection Worker..."
echo "Queue: object_detection"
echo "---"

celery -A app.celery_app worker \
    --queues=object_detection \
    --concurrency=2 \
    --loglevel=info \
    --hostname=object_worker@%h
