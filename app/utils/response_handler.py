"""
Response handling utilities for consistent API responses
"""
from datetime import datetime

from flask import jsonify


class ResponseHandler:
    """Utility class for standardized API responses"""

    @staticmethod
    def success(data=None, message='Success', status_code=200):
        """
        Create a success response

        Args:
            data: Response data
            message: Success message
            status_code: HTTP status code

        Returns:
            Flask response object
        """
        response = {
            'success': True,
            'message': message,
            'timestamp': datetime.utcnow().isoformat(),
        }

        if data is not None:
            response['data'] = data

        return jsonify(response), status_code

    @staticmethod
    def error(message='An error occurred', status_code=400, error_code=None):
        """
        Create an error response

        Args:
            message: Error message
            status_code: HTTP status code
            error_code: Optional error code

        Returns:
            Flask response object
        """
        response = {
            'success': False,
            'message': message,
            'timestamp': datetime.utcnow().isoformat(),
        }

        if error_code:
            response['error_code'] = error_code

        return jsonify(response), status_code

    @staticmethod
    def validation_error(errors, message='Validation failed'):
        """
        Create a validation error response

        Args:
            errors: List or dict of validation errors
            message: Error message

        Returns:
            Flask response object
        """
        response = {
            'success': False,
            'message': message,
            'errors': errors,
            'timestamp': datetime.utcnow().isoformat(),
        }

        return jsonify(response), 422

    @staticmethod
    def not_found(resource='Resource', message=None):
        """
        Create a not found response

        Args:
            resource: Name of the resource not found
            message: Optional custom message

        Returns:
            Flask response object
        """
        if message is None:
            message = f'{resource} not found'

        response = {
            'success': False,
            'message': message,
            'timestamp': datetime.utcnow().isoformat(),
        }

        return jsonify(response), 404

    @staticmethod
    def unauthorized(message='Unauthorized access'):
        """
        Create an unauthorized response

        Args:
            message: Error message

        Returns:
            Flask response object
        """
        response = {
            'success': False,
            'message': message,
            'timestamp': datetime.utcnow().isoformat(),
        }

        return jsonify(response), 401
