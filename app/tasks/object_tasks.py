"""
Celery tasks for object detection processing
These tasks run on dedicated object detection worker containers
"""
import logging

from app.celery_app import celery_app
from app.config import Config
from app.services import ObjectDetectionService

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name='app.tasks.object_tasks.detect_objects_in_image')
def detect_objects_in_image_task(self, image_path):
    """
    Asynchronous task to detect objects in an image

    Args:
        image_path: Path to the image file

    Returns:
        dict: Detection results
    """
    try:
        # Update task state
        self.update_state(state='PROCESSING', meta={'status': 'Initializing object detection service'})

        # Initialize service
        service = ObjectDetectionService(
            weights_path=Config.YOLO_WEIGHTS_PATH,
            config_path=Config.YOLO_CONFIG_PATH,
            names_path=Config.YOLO_NAMES_PATH,
            confidence_threshold=Config.OBJECT_DETECTION_CONFIDENCE,
            nms_threshold=Config.NMS_THRESHOLD
        )

        # Update state
        self.update_state(state='PROCESSING', meta={'status': 'Detecting objects in image'})

        # Process image
        result = service.detect_objects_in_image(image_path)

        logger.info(f"Object detection completed for {image_path}: {result.get('objects_detected', 0)} objects found")

        return result

    except Exception as e:
        logger.error(f"Error in object detection task: {e}")
        return {
            'success': False,
            'error': str(e),
            'objects_detected': 0
        }


@celery_app.task(bind=True, name='app.tasks.object_tasks.detect_objects_in_video')
def detect_objects_in_video_task(self, video_path, frame_skip=5):
    """
    Asynchronous task to detect objects in a video

    Args:
        video_path: Path to the video file
        frame_skip: Process every Nth frame

    Returns:
        dict: Detection results
    """
    try:
        # Update task state
        self.update_state(state='PROCESSING', meta={'status': 'Initializing object detection service'})

        # Initialize service
        service = ObjectDetectionService(
            weights_path=Config.YOLO_WEIGHTS_PATH,
            config_path=Config.YOLO_CONFIG_PATH,
            names_path=Config.YOLO_NAMES_PATH,
            confidence_threshold=Config.OBJECT_DETECTION_CONFIDENCE,
            nms_threshold=Config.NMS_THRESHOLD
        )

        # Update state
        self.update_state(state='PROCESSING', meta={'status': 'Processing video frames'})

        # Process video
        result = service.detect_objects_in_video(video_path, frame_skip=frame_skip)

        logger.info(f"Object detection completed for video {video_path}")

        return result

    except Exception as e:
        logger.error(f"Error in video object detection task: {e}")
        return {
            'success': False,
            'error': str(e)
        }
