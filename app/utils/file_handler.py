"""
File handling utilities for uploads and processing
"""
import os
from pathlib import Path
from werkzeug.utils import secure_filename
import uuid
import logging

logger = logging.getLogger(__name__)


class FileHandler:
    """Utility class for file handling operations"""

    @staticmethod
    def allowed_file(filename, allowed_extensions):
        """
        Check if a file has an allowed extension

        Args:
            filename: Name of the file
            allowed_extensions: Set of allowed extensions

        Returns:
            bool: True if file is allowed
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions

    @staticmethod
    def save_upload(file, upload_folder):
        """
        Save an uploaded file with a unique name

        Args:
            file: FileStorage object from Flask
            upload_folder: Directory to save the file

        Returns:
            Path: Path to the saved file
        """
        # Create upload folder if it doesn't exist
        os.makedirs(upload_folder, exist_ok=True)

        # Generate unique filename
        original_filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())[:8]
        name, ext = os.path.splitext(original_filename)
        filename = f"{name}_{unique_id}{ext}"

        filepath = Path(upload_folder) / filename
        file.save(str(filepath))

        logger.info(f"Saved file: {filepath}")
        return filepath

    @staticmethod
    def get_file_info(filepath):
        """
        Get information about a file

        Args:
            filepath: Path to the file

        Returns:
            dict: File information
        """
        path = Path(filepath)
        if not path.exists():
            return None

        return {
            'filename': path.name,
            'size': path.stat().st_size,
            'extension': path.suffix,
            'path': str(path)
        }

    @staticmethod
    def cleanup_file(filepath):
        """
        Remove a file from the filesystem

        Args:
            filepath: Path to the file to remove

        Returns:
            bool: True if file was removed
        """
        try:
            path = Path(filepath)
            if path.exists():
                path.unlink()
                logger.info(f"Removed file: {filepath}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error removing file {filepath}: {e}")
            return False

    @staticmethod
    def get_file_extension(filename):
        """
        Get the file extension

        Args:
            filename: Name of the file

        Returns:
            str: File extension without the dot
        """
        return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

    @staticmethod
    def is_image(filename):
        """
        Check if a file is an image

        Args:
            filename: Name of the file

        Returns:
            bool: True if file is an image
        """
        image_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}
        return FileHandler.get_file_extension(filename) in image_extensions

    @staticmethod
    def is_video(filename):
        """
        Check if a file is a video

        Args:
            filename: Name of the file

        Returns:
            bool: True if file is a video
        """
        video_extensions = {'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv', 'webm', 'mpeg'}
        return FileHandler.get_file_extension(filename) in video_extensions
