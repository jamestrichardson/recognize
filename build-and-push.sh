#!/usr/bin/env bash
# Build and push Docker containers to Docker Hub
# Usage: ./build-and-push.sh [version]
# Example: ./build-and-push.sh v1.0.0

set -euo pipefail
IFS=$'\n\t'

# Configuration
DOCKER_USERNAME="${DOCKER_USERNAME:-jamestrichardson}"
REGISTRY="${REGISTRY:-docker.io}"
VERSION="${1:-latest}"

# Image names
WEB_IMAGE="${REGISTRY}/${DOCKER_USERNAME}/recognize"
FACE_WORKER_IMAGE="${REGISTRY}/${DOCKER_USERNAME}/recognize-face-worker"
OBJECT_WORKER_IMAGE="${REGISTRY}/${DOCKER_USERNAME}/recognize-object-worker"

# Platforms to build for
PLATFORMS="linux/amd64,linux/arm64"

echo "=========================================="
echo "Building and Pushing Docker Images"
echo "=========================================="
echo "Registry: ${REGISTRY}"
echo "Username: ${DOCKER_USERNAME}"
echo "Version: ${VERSION}"
echo "Platforms: ${PLATFORMS}"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running"
    exit 1
fi

# Check if logged in to Docker Hub
if ! docker info 2>&1 | grep -q "Username: ${DOCKER_USERNAME}"; then
    echo "Not logged in to Docker Hub. Attempting login..."
    docker login
    echo ""
fi

# Set up Docker Buildx for multi-platform builds
echo "Setting up Docker Buildx..."
if ! docker buildx inspect recognize-builder > /dev/null 2>&1; then
    docker buildx create --name recognize-builder --use
else
    docker buildx use recognize-builder
fi
docker buildx inspect --bootstrap
echo ""

# Build and push web application
echo "Building and pushing web application..."
docker buildx build \
    --platform ${PLATFORMS} \
    --file ./Dockerfile \
    --tag ${WEB_IMAGE}:${VERSION} \
    --tag ${WEB_IMAGE}:latest \
    --push \
    .
echo "✓ Web application pushed"
echo ""

# Build and push face worker
echo "Building and pushing face worker..."
docker buildx build \
    --platform ${PLATFORMS} \
    --file ./Dockerfile.face-worker \
    --tag ${FACE_WORKER_IMAGE}:${VERSION} \
    --tag ${FACE_WORKER_IMAGE}:latest \
    --push \
    .
echo "✓ Face worker pushed"
echo ""

# Build and push object worker
echo "Building and pushing object worker..."
docker buildx build \
    --platform ${PLATFORMS} \
    --file ./Dockerfile.object-worker \
    --tag ${OBJECT_WORKER_IMAGE}:${VERSION} \
    --tag ${OBJECT_WORKER_IMAGE}:latest \
    --push \
    .
echo "✓ Object worker pushed"
echo ""

echo "=========================================="
echo "Build and Push Complete!"
echo "=========================================="
echo ""
echo "Images pushed:"
echo "  ${WEB_IMAGE}:${VERSION}"
echo "  ${WEB_IMAGE}:latest"
echo "  ${FACE_WORKER_IMAGE}:${VERSION}"
echo "  ${FACE_WORKER_IMAGE}:latest"
echo "  ${OBJECT_WORKER_IMAGE}:${VERSION}"
echo "  ${OBJECT_WORKER_IMAGE}:latest"
echo ""
echo "To pull and use:"
echo "  docker pull ${WEB_IMAGE}:${VERSION}"
echo "  docker pull ${FACE_WORKER_IMAGE}:${VERSION}"
echo "  docker pull ${OBJECT_WORKER_IMAGE}:${VERSION}"
echo ""
