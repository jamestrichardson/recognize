# Celery Tasks

This directory contains asynchronous task definitions for distributed processing.

## Task Modules

### `face_tasks.py`

Face detection tasks that run on dedicated face detection workers.

**Tasks:**

- `detect_faces_in_image_task(image_path)` - Detect faces in a single image
- `detect_faces_in_video_task(video_path, frame_skip)` - Detect faces in video

**Queue:** `face_detection`

### `object_tasks.py`

Object detection tasks that run on dedicated object detection workers.

**Tasks:**

- `detect_objects_in_image_task(image_path)` - Detect objects in a single image
- `detect_objects_in_video_task(video_path, frame_skip)` - Detect objects in video

**Queue:** `object_detection`

## Task Routing

Tasks are automatically routed to the correct queue based on their module:

```python
# Configured in app/celery_app.py
task_routes = {
    'app.tasks.face_tasks.*': {'queue': 'face_detection'},
    'app.tasks.object_tasks.*': {'queue': 'object_detection'},
}
```text

## Usage

### From Routes

```python
from app.tasks import detect_faces_in_image_task

# Queue the task
result = detect_faces_in_image_task.apply_async(args=['/path/to/image.jpg'])

# Get task ID
task_id = result.id

# Check status later
from celery.result import AsyncResult
task = AsyncResult(task_id)
status = task.state
```text

### From Python Shell

```python
from app.tasks import detect_objects_in_video_task

# Queue task
task = detect_objects_in_video_task.delay('/path/to/video.mp4', frame_skip=5)

# Check if ready
task.ready()

# Get result (blocks until complete)
result = task.get()
```text

## Task States

- `PENDING` - Task is waiting in queue
- `STARTED` - Worker has started processing
- `PROCESSING` - Task is actively running (custom state)
- `SUCCESS` - Task completed successfully
- `FAILURE` - Task failed with error
- `RETRY` - Task is being retried

## Adding New Tasks

1. Create new task function with `@celery_app.task` decorator
2. Add to `__init__.py` exports
3. Import in routes or other modules
4. Queue with `.apply_async()` or `.delay()`

Example:

```python
@celery_app.task(bind=True, name='app.tasks.face_tasks.new_task')
def new_face_task(self, param1, param2):
    self.update_state(state='PROCESSING', meta={'status': 'Starting...'})
    # Your code here
    return result
```text
