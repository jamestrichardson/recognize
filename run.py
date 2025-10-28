"""
Main entry point for the Recognize application
"""
import os

from app import create_app

# Create Flask app instance
app = create_app()

if __name__ == '__main__':
    # Get host and port from environment or use defaults
    host = os.getenv('FLASK_HOST', '0.0.0.0')  # nosec B104
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'

    print(f"Starting Recognize application on {host}:{port}")
    app.run(host=host, port=port, debug=debug)
