"""
Recognition services package
"""
from .facial_recognition import FacialRecognitionService
from .object_detection import ObjectDetectionService

__all__ = ['FacialRecognitionService', 'ObjectDetectionService']
