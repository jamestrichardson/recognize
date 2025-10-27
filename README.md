# Recognize - Object and Facial Recognition Application

A Flask-based web application for performing object detection and facial recognition on images and videos using computer vision techniques.

## Features

- **Face Detection**: Detect and locate faces in images and videos
- **Object Recognition**: Identify and classify objects using YOLO models
- **Video Processing**: Process video files frame-by-frame for comprehensive analysis
- **REST API**: Well-documented API endpoints for integration
- **Web Interface**: User-friendly web interface for file uploads and results viewing

## Project Structure

```
recognize/
├── app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Configuration settings
│   ├── routes.py            # API and web routes
│   ├── services/            # Recognition services
│   │   ├── facial_recognition.py
│   │   └── object_detection.py
│   ├── utils/               # Utility modules
│   │   ├── file_handler.py
│   │   └── response_handler.py
│   ├── static/              # CSS and JavaScript
│   └── templates/           # HTML templates
├── models/                  # Model files directory
├── uploads/                 # Uploaded files directory
├── tests/                   # Test suite
├── requirements.txt         # Python dependencies
├── .env.example            # Example environment variables
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
└── run.py                  # Application entry point
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd recognize
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the example environment file:
```bash
cp .env.example .env
```

5. Edit `.env` and configure your settings (especially `SECRET_KEY` for production)

### Model Files

Place the following model files in the `models/` directory:

- **For Face Detection**: `haarcascade_frontalface_default.xml` (included with OpenCV)
- **For Object Detection** (optional):
  - `yolov3.weights` - Download from [YOLO website](https://pjreddie.com/darknet/yolo/)
  - `yolov3.cfg` - Download from [YOLO repository](https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg)
  - `coco.names` - Download from [YOLO repository](https://github.com/pjreddie/darknet/blob/master/data/coco.names)

## Usage

### Running Locally

```bash
python run.py
```

The application will be available at `http://localhost:5000`

### Using Docker

Build and run with Docker Compose:

```bash
docker-compose up --build
```

### API Endpoints

#### Health Check
```
GET /api/health
```

#### Face Detection - Image
```
POST /api/detect/face/image
Content-Type: multipart/form-data
Body: file (image file)
```

#### Face Detection - Video
```
POST /api/detect/face/video
Content-Type: multipart/form-data
Body:
  - file (video file)
  - frame_skip (optional, default: 5)
```

#### Object Detection - Image
```
POST /api/detect/object/image
Content-Type: multipart/form-data
Body: file (image file)
```

#### Object Detection - Video
```
POST /api/detect/object/video
Content-Type: multipart/form-data
Body:
  - file (video file)
  - frame_skip (optional, default: 5)
```

## Configuration

Key configuration options in `.env`:

- `SECRET_KEY`: Flask secret key (required for production)
- `DEBUG`: Enable/disable debug mode
- `MAX_CONTENT_LENGTH`: Maximum file upload size (bytes)
- `FACE_DETECTION_CONFIDENCE`: Confidence threshold for face detection (0-1)
- `OBJECT_DETECTION_CONFIDENCE`: Confidence threshold for object detection (0-1)
- `VIDEO_FRAME_SKIP`: Process every Nth frame in videos

## Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app tests/
```

## Development

### Code Style

This project follows Python best practices. Format code with:

```bash
black app/ tests/
flake8 app/ tests/
```

### Adding New Features

1. Create feature branch
2. Implement changes
3. Add tests
4. Submit pull request

## Deployment

### Production Considerations

1. Set `DEBUG=False` in production
2. Use a strong `SECRET_KEY`
3. Configure proper file upload limits
4. Use a production WSGI server (gunicorn is included)
5. Set up reverse proxy (nginx recommended)
6. Enable HTTPS
7. Configure logging and monitoring

### Environment Variables

Ensure all required environment variables are set in your production environment.

## Troubleshooting

### Models not loading
- Verify model files are in the `models/` directory
- Check file paths in `.env` configuration
- Ensure proper file permissions

### Large file uploads failing
- Increase `MAX_CONTENT_LENGTH` in configuration
- Check web server upload limits

### Video processing slow
- Increase `VIDEO_FRAME_SKIP` to process fewer frames
- Consider using GPU-accelerated OpenCV

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on the repository.
