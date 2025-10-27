#!/usr/bin/env bash
# Start Celery face detection worker

echo "Starting Face Detection Worker..."
echo "Queue: face_detection"
echo "---"

celery -A app.celery_app worker \
    --queues=face_detection \
    --concurrency=2 \
    --loglevel=info \
    --hostname=face_worker@%h
