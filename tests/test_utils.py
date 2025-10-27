"""
Tests for utility modules
"""
from pathlib import Path

import pytest

from app.utils import FileHandler, ResponseHandler


def test_file_handler_allowed_file():
    """Test file extension validation"""
    assert FileHandler.allowed_file('test.jpg', {'jpg', 'png'}) is True
    assert FileHandler.allowed_file('test.txt', {'jpg', 'png'}) is False
    assert FileHandler.allowed_file('test', {'jpg', 'png'}) is False


def test_file_handler_get_file_extension():
    """Test getting file extension"""
    assert FileHandler.get_file_extension('test.jpg') == 'jpg'
    assert FileHandler.get_file_extension('test.PNG') == 'png'
    assert FileHandler.get_file_extension('test') == ''


def test_file_handler_is_image():
    """Test image file detection"""
    assert FileHandler.is_image('photo.jpg') is True
    assert FileHandler.is_image('photo.png') is True
    assert FileHandler.is_image('video.mp4') is False


def test_file_handler_is_video():
    """Test video file detection"""
    assert FileHandler.is_video('video.mp4') is True
    assert FileHandler.is_video('video.avi') is True
    assert FileHandler.is_video('photo.jpg') is False


def test_response_handler_success():
    """Test success response creation"""
    response, status_code = ResponseHandler.success({'key': 'value'})
    assert status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data


def test_response_handler_error():
    """Test error response creation"""
    response, status_code = ResponseHandler.error('Test error', 400)
    assert status_code == 400
    data = response.get_json()
    assert data['success'] is False
    assert data['message'] == 'Test error'


def test_response_handler_not_found():
    """Test not found response creation"""
    response, status_code = ResponseHandler.not_found('File')
    assert status_code == 404
    data = response.get_json()
    assert data['success'] is False
    assert 'not found' in data['message'].lower()
