"""
Flask routes for the Recognize application
"""
import logging

from flask import Blueprint, current_app, render_template, request, send_from_directory

from app.services import FacialRecognitionService, ObjectDetectionService
from app.utils.file_handler import FileHandler
from app.utils.response_handler import ResponseHandler

logger = logging.getLogger(__name__)

# Create blueprints
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

# Initialize services (will be properly configured on first use)
face_service = None
object_service = None


def get_face_service():
    """Get or initialize facial recognition service"""
    global face_service
    if face_service is None:
        face_service = FacialRecognitionService(
            cascade_path=current_app.config.get('FACE_CASCADE_PATH'),
            confidence_threshold=current_app.config.get('FACE_DETECTION_CONFIDENCE', 0.5)
        )
    return face_service


def get_object_service():
    """Get or initialize object detection service"""
    global object_service
    if object_service is None:
        object_service = ObjectDetectionService(
            weights_path=current_app.config.get('YOLO_WEIGHTS_PATH'),
            config_path=current_app.config.get('YOLO_CONFIG_PATH'),
            names_path=current_app.config.get('YOLO_NAMES_PATH'),
            confidence_threshold=current_app.config.get('OBJECT_DETECTION_CONFIDENCE', 0.5),
            nms_threshold=current_app.config.get('NMS_THRESHOLD', 0.4)
        )
    return object_service


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
    face_svc = get_face_service()
    obj_svc = get_object_service()

    return ResponseHandler.success({
        'status': 'healthy',
        'services': {
            'facial_recognition': face_svc.is_available(),
            'object_detection': obj_svc.is_available()
        }
    })


@api_bp.route('/detect/face/image', methods=['POST'])
def detect_face_image():
    """Detect faces in an uploaded image"""
    try:
        # Validate and save file
        if 'file' not in request.files:
            return ResponseHandler.error('No file provided', 400)

        file = request.files['file']
        if file.filename == '':
            return ResponseHandler.error('No file selected', 400)

        # Validate file type
        allowed_exts = current_app.config['ALLOWED_IMAGE_EXTENSIONS']
        if not FileHandler.allowed_file(file.filename, allowed_exts):
            return ResponseHandler.error(
                f"Invalid file type. Allowed: {', '.join(allowed_exts)}",
                400
            )

        # Save file
        filepath = FileHandler.save_upload(file, current_app.config['UPLOAD_FOLDER'])

        # Process image
        face_svc = get_face_service()
        if not face_svc.is_available():
            return ResponseHandler.error('Facial recognition service not available', 503)

        result = face_svc.detect_faces_in_image(filepath)

        if result['success']:
            return ResponseHandler.success(result)
        else:
            return ResponseHandler.error(result.get('error', 'Detection failed'), 500)

    except Exception as e:
        logger.error(f"Error in face detection: {e}")
        return ResponseHandler.error(str(e), 500)


@api_bp.route('/detect/face/video', methods=['POST'])
def detect_face_video():
    """Detect faces in an uploaded video"""
    try:
        # Validate and save file
        if 'file' not in request.files:
            return ResponseHandler.error('No file provided', 400)

        file = request.files['file']
        if file.filename == '':
            return ResponseHandler.error('No file selected', 400)

        # Validate file type
        allowed_exts = current_app.config['ALLOWED_VIDEO_EXTENSIONS']
        if not FileHandler.allowed_file(file.filename, allowed_exts):
            return ResponseHandler.error(
                f"Invalid file type. Allowed: {', '.join(allowed_exts)}",
                400
            )

        # Save file
        filepath = FileHandler.save_upload(file, current_app.config['UPLOAD_FOLDER'])

        # Get frame skip parameter
        frame_skip = request.form.get(
            'frame_skip',
            current_app.config.get('VIDEO_FRAME_SKIP', 5),
            type=int
        )

        # Process video
        face_svc = get_face_service()
        if not face_svc.is_available():
            return ResponseHandler.error('Facial recognition service not available', 503)

        result = face_svc.detect_faces_in_video(filepath, frame_skip=frame_skip)

        if result['success']:
            return ResponseHandler.success(result)
        else:
            return ResponseHandler.error(result.get('error', 'Detection failed'), 500)

    except Exception as e:
        logger.error(f"Error in face detection: {e}")
        return ResponseHandler.error(str(e), 500)


@api_bp.route('/detect/object/image', methods=['POST'])
def detect_object_image():
    """Detect objects in an uploaded image"""
    try:
        # Validate and save file
        if 'file' not in request.files:
            return ResponseHandler.error('No file provided', 400)

        file = request.files['file']
        if file.filename == '':
            return ResponseHandler.error('No file selected', 400)

        # Validate file type
        allowed_exts = current_app.config['ALLOWED_IMAGE_EXTENSIONS']
        if not FileHandler.allowed_file(file.filename, allowed_exts):
            return ResponseHandler.error(
                f"Invalid file type. Allowed: {', '.join(allowed_exts)}",
                400
            )

        # Save file
        filepath = FileHandler.save_upload(file, current_app.config['UPLOAD_FOLDER'])

        # Process image
        obj_svc = get_object_service()
        if not obj_svc.is_available():
            return ResponseHandler.error('Object detection service not available', 503)

        result = obj_svc.detect_objects_in_image(filepath)

        if result['success']:
            return ResponseHandler.success(result)
        else:
            return ResponseHandler.error(result.get('error', 'Detection failed'), 500)

    except Exception as e:
        logger.error(f"Error in object detection: {e}")
        return ResponseHandler.error(str(e), 500)


@api_bp.route('/detect/object/video', methods=['POST'])
def detect_object_video():
    """Detect objects in an uploaded video"""
    try:
        # Validate and save file
        if 'file' not in request.files:
            return ResponseHandler.error('No file provided', 400)

        file = request.files['file']
        if file.filename == '':
            return ResponseHandler.error('No file selected', 400)

        # Validate file type
        allowed_exts = current_app.config['ALLOWED_VIDEO_EXTENSIONS']
        if not FileHandler.allowed_file(file.filename, allowed_exts):
            return ResponseHandler.error(
                f"Invalid file type. Allowed: {', '.join(allowed_exts)}",
                400
            )

        # Save file
        filepath = FileHandler.save_upload(file, current_app.config['UPLOAD_FOLDER'])

        # Get frame skip parameter
        frame_skip = request.form.get(
            'frame_skip',
            current_app.config.get('VIDEO_FRAME_SKIP', 5),
            type=int
        )

        # Process video
        obj_svc = get_object_service()
        if not obj_svc.is_available():
            return ResponseHandler.error('Object detection service not available', 503)

        result = obj_svc.detect_objects_in_video(filepath, frame_skip=frame_skip)

        if result['success']:
            return ResponseHandler.success(result)
        else:
            return ResponseHandler.error(result.get('error', 'Detection failed'), 500)

    except Exception as e:
        logger.error(f"Error in object detection: {e}")
        return ResponseHandler.error(str(e), 500)


@api_bp.route('/uploads/<filename>', methods=['GET'])
def download_file(filename):
    """Serve uploaded or processed files"""
    try:
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
    except Exception as e:
        logger.error(f"Error serving file: {e}")
        return ResponseHandler.error('File not found', 404)
