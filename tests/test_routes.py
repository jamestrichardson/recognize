"""
Tests for Flask application routes
"""
import pytest

from app import create_app
from app.config import TestingConfig


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app(TestingConfig)
    yield app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


def test_index_route(client):
    """Test the index route"""
    response = client.get('/')
    assert response.status_code == 200


def test_upload_route(client):
    """Test the upload page route"""
    response = client.get('/upload')
    assert response.status_code == 200


def test_health_check(client):
    """Test the API health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'services' in data['data']


def test_face_detection_no_file(client):
    """Test face detection endpoint without file"""
    response = client.post('/api/detect/face/image')
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False


def test_object_detection_no_file(client):
    """Test object detection endpoint without file"""
    response = client.post('/api/detect/object/image')
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False
