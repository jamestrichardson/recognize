"""
Task modules for distributed processing
"""
from .face_tasks import detect_faces_in_image_task, detect_faces_in_video_task
from .object_tasks import detect_objects_in_image_task, detect_objects_in_video_task

__all__ = [
    'detect_faces_in_image_task',
    'detect_faces_in_video_task',
    'detect_objects_in_image_task',
    'detect_objects_in_video_task'
]
