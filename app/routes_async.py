"""
Flask routes for the Recognize application - Async version with Celery tasks
"""
from flask import Blueprint, render_template, request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
from pathlib import Path
import logging
import os
from app.utils.file_handler import FileHandler
from app.utils.response_handler import ResponseHandler

logger = logging.getLogger(__name__)

# Create blueprints
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

# Import Celery tasks (lazy import to avoid circular dependencies)
def get_celery_tasks():
    """Lazy import of Celery tasks"""
    try:
        from app.tasks import (
            detect_faces_in_image_task,
            detect_faces_in_video_task,
            detect_objects_in_image_task,
            detect_objects_in_video_task
        )
        return {
            'face_image': detect_faces_in_image_task,
            'face_video': detect_faces_in_video_task,
            'object_image': detect_objects_in_image_task,
            'object_video': detect_objects_in_video_task
        }
    except ImportError:
        logger.warning("Celery tasks not available - running in synchronous mode")
        return None


# Web Interface Routes
@main_bp.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@main_bp.route('/upload')
def upload_page():
    """Render the upload page"""
    return render_template('upload.html')


@main_bp.route('/results/<filename>')
def results_page(filename):
    """Render the results page"""
    return render_template('results.html', filename=filename)


# API Routes
@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    tasks = get_celery_tasks()

    return ResponseHandler.success({
        'status': 'healthy',
        'mode': 'async' if tasks else 'sync',
        'services': {
            'task_queue': tasks is not None,
        }
    })


@api_bp.route('/detect/face/image', methods=['POST'])
def detect_face_image():
    """Detect faces in an uploaded image - async with Celery"""
    try:
        # Validate and save file
        if 'file' not in request.files:
            return ResponseHandler.error('No file provided', 400)

        file = request.files['file']
        if file.filename == '':
            return ResponseHandler.error('No file selected', 400)

        # Validate file type
        if not FileHandler.allowed_file(file.filename, current_app.config['ALLOWED_IMAGE_EXTENSIONS']):
            return ResponseHandler.error('Invalid file type. Allowed: ' +
                                        ', '.join(current_app.config['ALLOWED_IMAGE_EXTENSIONS']), 400)

        # Save file
        filepath = FileHandler.save_upload(file, current_app.config['UPLOAD_FOLDER'])

        # Get Celery tasks
        tasks = get_celery_tasks()

        if tasks:
            # Async mode - queue the task
            task = tasks['face_image'].apply_async(args=[str(filepath)])

            return ResponseHandler.success({
                'task_id': task.id,
                'status': 'queued',
                'message': 'Face detection task queued. Use task_id to check status.'
            }, status_code=202)
        else:
            # Fallback to synchronous mode
            from app.services import FacialRecognitionService
            service = FacialRecognitionService(
                cascade_path=current_app.config.get('FACE_CASCADE_PATH'),
                confidence_threshold=current_app.config.get('FACE_DETECTION_CONFIDENCE', 0.5)
            )
            result = service.detect_faces_in_image(filepath)

            if result['success']:
                return ResponseHandler.success(result)
            else:
                return ResponseHandler.error(result.get('error', 'Detection failed'), 500)

    except Exception as e:
        logger.error(f"Error in face detection: {e}")
        return ResponseHandler.error(str(e), 500)


@api_bp.route('/detect/face/video', methods=['POST'])
def detect_face_video():
    """Detect faces in an uploaded video - async with Celery"""
    try:
        # Validate and save file
        if 'file' not in request.files:
            return ResponseHandler.error('No file provided', 400)

        file = request.files['file']
        if file.filename == '':
            return ResponseHandler.error('No file selected', 400)

        # Validate file type
        if not FileHandler.allowed_file(file.filename, current_app.config['ALLOWED_VIDEO_EXTENSIONS']):
            return ResponseHandler.error('Invalid file type. Allowed: ' +
                                        ', '.join(current_app.config['ALLOWED_VIDEO_EXTENSIONS']), 400)

        # Save file
        filepath = FileHandler.save_upload(file, current_app.config['UPLOAD_FOLDER'])

        # Get frame skip parameter
        frame_skip = request.form.get('frame_skip', current_app.config.get('VIDEO_FRAME_SKIP', 5), type=int)

        # Get Celery tasks
        tasks = get_celery_tasks()

        if tasks:
            # Async mode - queue the task
            task = tasks['face_video'].apply_async(args=[str(filepath), frame_skip])

            return ResponseHandler.success({
                'task_id': task.id,
                'status': 'queued',
                'message': 'Face detection task queued. Use task_id to check status.'
            }, status_code=202)
        else:
            # Fallback to synchronous mode
            from app.services import FacialRecognitionService
            service = FacialRecognitionService(
                cascade_path=current_app.config.get('FACE_CASCADE_PATH'),
                confidence_threshold=current_app.config.get('FACE_DETECTION_CONFIDENCE', 0.5)
            )
            result = service.detect_faces_in_video(filepath, frame_skip=frame_skip)

            if result['success']:
                return ResponseHandler.success(result)
            else:
                return ResponseHandler.error(result.get('error', 'Detection failed'), 500)

    except Exception as e:
        logger.error(f"Error in face detection: {e}")
        return ResponseHandler.error(str(e), 500)


@api_bp.route('/detect/object/image', methods=['POST'])
def detect_object_image():
    """Detect objects in an uploaded image - async with Celery"""
    try:
        # Validate and save file
        if 'file' not in request.files:
            return ResponseHandler.error('No file provided', 400)

        file = request.files['file']
        if file.filename == '':
            return ResponseHandler.error('No file selected', 400)

        # Validate file type
        if not FileHandler.allowed_file(file.filename, current_app.config['ALLOWED_IMAGE_EXTENSIONS']):
            return ResponseHandler.error('Invalid file type. Allowed: ' +
                                        ', '.join(current_app.config['ALLOWED_IMAGE_EXTENSIONS']), 400)

        # Save file
        filepath = FileHandler.save_upload(file, current_app.config['UPLOAD_FOLDER'])

        # Get Celery tasks
        tasks = get_celery_tasks()

        if tasks:
            # Async mode - queue the task
            task = tasks['object_image'].apply_async(args=[str(filepath)])

            return ResponseHandler.success({
                'task_id': task.id,
                'status': 'queued',
                'message': 'Object detection task queued. Use task_id to check status.'
            }, status_code=202)
        else:
            # Fallback to synchronous mode
            from app.services import ObjectDetectionService
            service = ObjectDetectionService(
                weights_path=current_app.config.get('YOLO_WEIGHTS_PATH'),
                config_path=current_app.config.get('YOLO_CONFIG_PATH'),
                names_path=current_app.config.get('YOLO_NAMES_PATH'),
                confidence_threshold=current_app.config.get('OBJECT_DETECTION_CONFIDENCE', 0.5),
                nms_threshold=current_app.config.get('NMS_THRESHOLD', 0.4)
            )
            result = service.detect_objects_in_image(filepath)

            if result['success']:
                return ResponseHandler.success(result)
            else:
                return ResponseHandler.error(result.get('error', 'Detection failed'), 500)

    except Exception as e:
        logger.error(f"Error in object detection: {e}")
        return ResponseHandler.error(str(e), 500)


@api_bp.route('/detect/object/video', methods=['POST'])
def detect_object_video():
    """Detect objects in an uploaded video - async with Celery"""
    try:
        # Validate and save file
        if 'file' not in request.files:
            return ResponseHandler.error('No file provided', 400)

        file = request.files['file']
        if file.filename == '':
            return ResponseHandler.error('No file selected', 400)

        # Validate file type
        if not FileHandler.allowed_file(file.filename, current_app.config['ALLOWED_VIDEO_EXTENSIONS']):
            return ResponseHandler.error('Invalid file type. Allowed: ' +
                                        ', '.join(current_app.config['ALLOWED_VIDEO_EXTENSIONS']), 400)

        # Save file
        filepath = FileHandler.save_upload(file, current_app.config['UPLOAD_FOLDER'])

        # Get frame skip parameter
        frame_skip = request.form.get('frame_skip', current_app.config.get('VIDEO_FRAME_SKIP', 5), type=int)

        # Get Celery tasks
        tasks = get_celery_tasks()

        if tasks:
            # Async mode - queue the task
            task = tasks['object_video'].apply_async(args=[str(filepath), frame_skip])

            return ResponseHandler.success({
                'task_id': task.id,
                'status': 'queued',
                'message': 'Object detection task queued. Use task_id to check status.'
            }, status_code=202)
        else:
            # Fallback to synchronous mode
            from app.services import ObjectDetectionService
            service = ObjectDetectionService(
                weights_path=current_app.config.get('YOLO_WEIGHTS_PATH'),
                config_path=current_app.config.get('YOLO_CONFIG_PATH'),
                names_path=current_app.config.get('YOLO_NAMES_PATH'),
                confidence_threshold=current_app.config.get('OBJECT_DETECTION_CONFIDENCE', 0.5),
                nms_threshold=current_app.config.get('NMS_THRESHOLD', 0.4)
            )
            result = service.detect_objects_in_video(filepath, frame_skip=frame_skip)

            if result['success']:
                return ResponseHandler.success(result)
            else:
                return ResponseHandler.error(result.get('error', 'Detection failed'), 500)

    except Exception as e:
        logger.error(f"Error in object detection: {e}")
        return ResponseHandler.error(str(e), 500)


@api_bp.route('/task/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """Get the status of a Celery task"""
    try:
        from celery.result import AsyncResult
        from app.celery_app import celery_app

        task = AsyncResult(task_id, app=celery_app)

        if task.state == 'PENDING':
            response = {
                'state': task.state,
                'status': 'Task is waiting in queue...'
            }
        elif task.state == 'PROCESSING':
            response = {
                'state': task.state,
                'status': task.info.get('status', 'Processing...') if isinstance(task.info, dict) else 'Processing...'
            }
        elif task.state == 'SUCCESS':
            response = {
                'state': task.state,
                'result': task.result
            }
        elif task.state == 'FAILURE':
            response = {
                'state': task.state,
                'status': str(task.info)
            }
        else:
            response = {
                'state': task.state,
                'status': 'Unknown state'
            }

        return ResponseHandler.success(response)

    except ImportError:
        return ResponseHandler.error('Task queue not available', 503)
    except Exception as e:
        logger.error(f"Error checking task status: {e}")
        return ResponseHandler.error(str(e), 500)


@api_bp.route('/uploads/<filename>', methods=['GET'])
def download_file(filename):
    """Serve uploaded or processed files"""
    try:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        logger.error(f"Error serving file: {e}")
        return ResponseHandler.error('File not found', 404)
