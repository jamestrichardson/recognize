"""
Celery tasks for facial recognition processing
These tasks run on dedicated face detection worker containers
"""
from app.celery_app import celery_app
from app.services import FacialRecognitionService
from app.config import Config
import logging

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name='app.tasks.face_tasks.detect_faces_in_image')
def detect_faces_in_image_task(self, image_path):
    """
    Asynchronous task to detect faces in an image

    Args:
        image_path: Path to the image file

    Returns:
        dict: Detection results
    """
    try:
        # Update task state
        self.update_state(state='PROCESSING', meta={'status': 'Initializing face detection service'})

        # Initialize service
        service = FacialRecognitionService(
            cascade_path=Config.FACE_CASCADE_PATH,
            confidence_threshold=Config.FACE_DETECTION_CONFIDENCE
        )

        # Update state
        self.update_state(state='PROCESSING', meta={'status': 'Detecting faces in image'})

        # Process image
        result = service.detect_faces_in_image(image_path)

        logger.info(f"Face detection completed for {image_path}: {result.get('faces_detected', 0)} faces found")

        return result

    except Exception as e:
        logger.error(f"Error in face detection task: {e}")
        return {
            'success': False,
            'error': str(e),
            'faces_detected': 0
        }


@celery_app.task(bind=True, name='app.tasks.face_tasks.detect_faces_in_video')
def detect_faces_in_video_task(self, video_path, frame_skip=5):
    """
    Asynchronous task to detect faces in a video

    Args:
        video_path: Path to the video file
        frame_skip: Process every Nth frame

    Returns:
        dict: Detection results
    """
    try:
        # Update task state
        self.update_state(state='PROCESSING', meta={'status': 'Initializing face detection service'})

        # Initialize service
        service = FacialRecognitionService(
            cascade_path=Config.FACE_CASCADE_PATH,
            confidence_threshold=Config.FACE_DETECTION_CONFIDENCE
        )

        # Update state
        self.update_state(state='PROCESSING', meta={'status': 'Processing video frames'})

        # Process video
        result = service.detect_faces_in_video(video_path, frame_skip=frame_skip)

        logger.info(f"Face detection completed for video {video_path}")

        return result

    except Exception as e:
        logger.error(f"Error in video face detection task: {e}")
        return {
            'success': False,
            'error': str(e)
        }
