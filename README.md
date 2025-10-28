# Recognize - Object and Facial Recognition Application

A Flask-based web application for performing object detection and facial recognition on images and videos using computer vision techniques.

## Features

- **Face Detection**: Detect and locate faces in images and videos
- **Object Recognition**: Identify and classify objects using YOLO models
- **Video Processing**: Process video files frame-by-frame for comprehensive analysis
- **REST API**: Well-documented API endpoints for integration
- **Web Interface**: User-friendly web interface for file uploads and results viewing
- **Scalable Architecture**: Separate worker containers for distributed processing (optional)
- **Async Task Queue**: Handle high load with Celery and Redis
- **Automated Releases**: Semantic versioning with Release Please
- **Code Quality**: Pre-commit hooks with conventional commits enforcement

## Documentation

- 📖 [Scalable Architecture Guide](SCALABLE_ARCHITECTURE.md) - Detailed architecture documentation
- 🚀 [Quick Start Guide](QUICKSTART_SCALABLE.md) - Get up and running quickly
- 🔧 [Pre-commit Setup](PRE_COMMIT_GUIDE.md) - Code quality automation
- 📝 [Conventional Commits](CONVENTIONAL_COMMITS.md) - Commit message standards
- 🎯 [Release Process](RELEASE_SETUP.md) - Automated release workflow
- 🔒 [Docker Security](DOCKER_SECURITY.md) - Container security best practices

## Architecture Modes

### 1. Simple Mode (Default)

- Single container deployment
- Synchronous processing
- Good for: Development, low traffic, quick setup

### 2. Scalable Mode (Production)

- Multiple service containers (web, redis, face workers, object workers)
- Asynchronous task processing with Celery
- Independent scaling of face/object detection workers
- Good for: Production, high traffic, compute-intensive workloads

📖 **See [SCALABLE_ARCHITECTURE.md](SCALABLE_ARCHITECTURE.md) for detailed architecture guide**

🚀 **See [QUICKSTART_SCALABLE.md](QUICKSTART_SCALABLE.md) for quick setup instructions**

## Project Structure

```text
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
```text

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```text

1. Install dependencies:

```bash
pip install -r requirements.txt
```text

1. Copy the example environment file:

```bash
cp .env.example .env
```text

1. Edit `.env` and configure your settings (especially `SECRET_KEY` for production)

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
```text

The application will be available at `http://localhost:5000`

### Using Docker

Build and run with Docker Compose:

```bash
docker-compose up --build
```text

### API Endpoints

#### Health Check

```text
GET /api/health
```text

#### Face Detection - Image

```text
POST /api/detect/face/image
Content-Type: multipart/form-data
Body: file (image file)
```text

#### Face Detection - Video

```text
POST /api/detect/face/video
Content-Type: multipart/form-data
Body:
  - file (video file)
  - frame_skip (optional, default: 5)
```text

#### Object Detection - Image

```text
POST /api/detect/object/image
Content-Type: multipart/form-data
Body: file (image file)
```text

#### Object Detection - Video

```text
POST /api/detect/object/video
Content-Type: multipart/form-data
Body:
  - file (video file)
  - frame_skip (optional, default: 5)
```text

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
```text

Run with coverage:

```bash
pytest --cov=app tests/
```text

## Development

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. The hooks run automatically before each commit and check:

- **Code Formatting**: Black, isort
- **Linting**: Flake8, pylint
- **Type Checking**: mypy
- **Security**: Bandit
- **Documentation**: Docstring coverage
- **Commit Messages**: Conventional Commits validation
- **Files**: Trailing whitespace, YAML/JSON validation, merge conflicts

#### Quick Setup

Run the automated setup script:

```bash
./setup-dev.sh
```text

Or manually install hooks:

```bash
pip install pre-commit
make install-hooks  # Installs both pre-commit and commit-msg hooks
```text

### Conventional Commits

All commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/) specification.
This enables automated versioning and changelog generation.

#### Commit Format

```text
<type>[optional scope]: <description>

[optional body]
[optional footer(s)]
```text

#### Common Types

- `feat:` - New feature (minor version bump)
- `fix:` - Bug fix (patch version bump)
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Test additions or modifications
- `chore:` - Maintenance tasks

#### Examples

```bash
git commit -m "feat: add video thumbnail generation"
git commit -m "fix(api): correct rate limiting logic"
git commit -m "docs: update deployment instructions"
```text

For breaking changes:

```bash
git commit -m "feat!: change API response format"
```text

📖 **See [CONVENTIONAL_COMMITS.md](CONVENTIONAL_COMMITS.md) for detailed guide**

#### Running Checks Manually

```bash
# Run all hooks on all files
make lint

# Run specific hooks
make format          # Format code with black and isort
make type-check      # Run mypy type checking
make security-check  # Run bandit security scan

# Auto-fix all issues
make format-fix
```text

#### Using Makefile Commands

The project includes a comprehensive Makefile for common development tasks:

```bash
# Setup and installation
make install         # Install dependencies
make install-dev     # Install dev dependencies
make install-hooks   # Install pre-commit hooks

# Code quality
make lint           # Run all linters
make format         # Check code formatting
make format-fix     # Fix formatting issues
make type-check     # Type checking with mypy
make security-check # Security scanning

# Testing
make test           # Run tests
make test-cov       # Run tests with coverage
make test-watch     # Run tests in watch mode

# Docker operations
make docker-build   # Build docker images
make docker-up      # Start containers (simple mode)
make docker-scale   # Start scalable architecture
make docker-down    # Stop containers

# Cleanup
make clean          # Remove cache files
make clean-all      # Deep clean including venv
```text

📖 **See [PRE_COMMIT_GUIDE.md](PRE_COMMIT_GUIDE.md) for detailed pre-commit documentation**

### Code Style

This project follows Python best practices:

- **Line length**: 100 characters
- **Import order**: Standard library → Third-party → Local (enforced by isort)
- **Formatting**: Black (opinionated formatter)
- **Docstrings**: Google-style docstrings required for public functions

### Adding New Features

1. Create feature branch from main
1. Install pre-commit hooks (`make install-hooks`)
1. Implement changes with conventional commits
1. Write tests (pytest)
1. Ensure all checks pass (`make ci`)
1. Submit pull request

## Release Process

This project uses automated releases with [Release Please](https://github.com/googleapis/release-please).

### How It Works

1. **Commit with conventional commits**: All commits to `main` branch
1. **Automatic PR creation**: Release Please analyzes commits and creates/updates a release PR
1. **Version bump**: Determined by commit types (feat = minor, fix = patch, BREAKING CHANGE = major)
1. **Changelog generation**: Automatically generated from commit messages
1. **GitHub release**: Created when release PR is merged

### Release Types

- `fix:` commits → Patch release (0.0.X)
- `feat:` commits → Minor release (0.X.0)
- `BREAKING CHANGE:` or `!` → Major release (X.0.0)

### Triggering a Release

Simply merge the auto-generated "chore(main): release X.X.X" pull request. The release workflow will:

- Create a GitHub release with auto-generated notes
- Tag the release with version number
- Update version in `app/version.py`
- Maintain CHANGELOG.md

No manual version bumping or changelog editing required!

## Deployment

### Production Considerations

1. Set `DEBUG=False` in production
1. Use a strong `SECRET_KEY`
1. Configure proper file upload limits
1. Use a production WSGI server (gunicorn is included)
1. Set up reverse proxy (nginx recommended)
1. Enable HTTPS
1. Configure logging and monitoring

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
