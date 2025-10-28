"""
Configuration settings for the Recognize application
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """Base configuration"""

    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

    # File upload settings
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', str(BASE_DIR / 'uploads'))
    PROCESSED_FOLDER = os.getenv('PROCESSED_FOLDER', str(BASE_DIR / 'uploads' / 'processed'))
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 100 * 1024 * 1024))  # 100MB default
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv'}

    # Model paths
    MODELS_DIR = os.getenv('MODELS_DIR', str(BASE_DIR / 'models'))
    FACE_CASCADE_PATH = os.getenv(
        'FACE_CASCADE_PATH',
        str(Path(MODELS_DIR) / 'haarcascade_frontalface_default.xml')
    )
    YOLO_WEIGHTS_PATH = os.getenv('YOLO_WEIGHTS_PATH', str(Path(MODELS_DIR) / 'yolov3.weights'))
    YOLO_CONFIG_PATH = os.getenv('YOLO_CONFIG_PATH', str(Path(MODELS_DIR) / 'yolov3.cfg'))
    YOLO_NAMES_PATH = os.getenv('YOLO_NAMES_PATH', str(Path(MODELS_DIR) / 'coco.names'))

    # Recognition settings
    FACE_DETECTION_CONFIDENCE = float(os.getenv('FACE_DETECTION_CONFIDENCE', 0.5))
    OBJECT_DETECTION_CONFIDENCE = float(os.getenv('OBJECT_DETECTION_CONFIDENCE', 0.5))
    NMS_THRESHOLD = float(os.getenv('NMS_THRESHOLD', 0.4))

    # Processing settings
    MAX_IMAGE_DIMENSION = int(os.getenv('MAX_IMAGE_DIMENSION', 1920))
    VIDEO_FRAME_SKIP = int(os.getenv('VIDEO_FRAME_SKIP', 5))  # Process every Nth frame

    # API settings
    API_RATE_LIMIT = os.getenv('API_RATE_LIMIT', '100 per hour')

    # Celery / Task Queue settings
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', str(BASE_DIR / 'recognize.log'))


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    UPLOAD_FOLDER = str(BASE_DIR / 'tests' / 'uploads')


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
