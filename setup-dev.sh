#!/usr/bin/env bash
# Setup script for pre-commit hooks and development environment

set -e

echo "=========================================="
echo "Setting up development environment"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $python_version"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Install pre-commit
echo "Installing pre-commit..."
pip install -q pre-commit
echo "✓ Pre-commit installed"
echo ""

# Install git hooks
echo "Installing pre-commit hooks..."
pre-commit install
pre-commit install --hook-type commit-msg
echo "✓ Git hooks installed"
echo ""

# Install hook environments (this may take a few minutes)
echo "Installing hook environments (this may take a few minutes)..."
pre-commit install --install-hooks
echo "✓ Hook environments installed"
echo ""

echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Available commands:"
echo "  make help           - Show all available commands"
echo "  make lint           - Run all linters"
echo "  make format         - Format code"
echo "  make test           - Run tests"
echo "  make pre-commit     - Run pre-commit on all files"
echo ""
echo "Pre-commit hooks are now active!"
echo "They will run automatically on 'git commit'"
echo ""
echo "To run manually: pre-commit run --all-files"
echo ""
