"""
Tests for service modules
"""
import pytest
from pathlib import Path
from app.services import FacialRecognitionService, ObjectDetectionService


def test_facial_recognition_service_init():
    """Test facial recognition service initialization"""
    service = FacialRecognitionService()
    assert service is not None
    assert hasattr(service, 'face_cascade')


def test_object_detection_service_init():
    """Test object detection service initialization"""
    service = ObjectDetectionService()
    assert service is not None
    assert hasattr(service, 'net')


def test_facial_recognition_is_available():
    """Test if facial recognition service is available"""
    service = FacialRecognitionService()
    # Service should be available with default cascade
    assert isinstance(service.is_available(), bool)


def test_object_detection_is_available():
    """Test if object detection service is available"""
    service = ObjectDetectionService()
    # Service may not be available without models
    assert isinstance(service.is_available(), bool)
