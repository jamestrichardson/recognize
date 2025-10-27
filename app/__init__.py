"""
Recognize - Object and Facial Recognition Application
Flask application factory and initialization
"""
import os

from flask import Flask
from flask_cors import CORS

from .config import Config


def create_app(config_class=Config):
    """
    Application factory pattern for Flask app

    Args:
        config_class: Configuration class to use

    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CORS
    CORS(app)

    # Ensure upload directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

    # Register blueprints
    from app.routes import api_bp, main_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    # Register error handlers
    register_error_handlers(app)

    return app


def register_error_handlers(app):
    """Register error handlers for the application"""

    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Resource not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal server error"}, 500

    @app.errorhandler(413)
    def file_too_large(error):
        return {"error": "File too large"}, 413
