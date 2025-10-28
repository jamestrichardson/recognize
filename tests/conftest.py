"""
Pytest configuration and fixtures
"""
import pytest

from app import create_app


@pytest.fixture
def app():
    """Create and configure a test Flask app instance"""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SECRET_KEY': 'test-secret-key',
    })
    yield app


@pytest.fixture
def client(app):
    """Create a test client for the app"""
    return app.test_client()


@pytest.fixture
def app_context(app):
    """Create an application context"""
    with app.app_context():
        yield app
