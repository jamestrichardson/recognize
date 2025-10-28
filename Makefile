.PHONY: help install install-dev install-hooks lint format test test-cov clean run docker-up docker-down docker-scale

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	pip install -r requirements.txt

install-dev: ## Install all dependencies including dev tools
	pip install -r requirements.txt
	pip install pre-commit

install-hooks: ## Install pre-commit hooks
	pre-commit install
	pre-commit install --hook-type commit-msg
	@echo "✓ Pre-commit hooks installed (including conventional commits validation)"

lint: ## Run all linters
	@echo "Running flake8..."
	flake8 app/ tests/
	@echo "Running pylint..."
	pylint app/ tests/ --disable=C0111,R0903,R0913
	@echo "Running mypy..."
	mypy app/
	@echo "Running bandit..."
	bandit -r app/ -c pyproject.toml
	@echo "Running isort check..."
	isort --check-only --diff app/ tests/
	@echo "Running black check..."
	black --check app/ tests/

format: ## Format code with black and isort
	@echo "Running isort..."
	isort app/ tests/
	@echo "Running black..."
	black app/ tests/

test: ## Run tests
	pytest tests/ -v

test-cov: ## Run tests with coverage
	pytest tests/ -v --cov=app --cov-report=html --cov-report=term

clean: ## Clean up temporary files and caches
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info

run: ## Run the Flask application locally
	python run.py

docker-up: ## Start all services with docker-compose
	docker-compose up --build

docker-up-scalable: ## Start scalable architecture with docker-compose
	docker-compose -f docker-compose.scalable.yml up --build

docker-down: ## Stop all docker services
	docker-compose down
	docker-compose -f docker-compose.scalable.yml down

docker-scale: ## Scale workers (usage: make docker-scale FACE=5 OBJECT=3)
	docker-compose -f docker-compose.scalable.yml up --scale face-worker=$(FACE) --scale object-worker=$(OBJECT) -d

pre-commit: ## Run pre-commit on all files
	pre-commit run --all-files

pre-commit-update: ## Update pre-commit hooks
	pre-commit autoupdate

commit-help: ## Show conventional commits quick reference
	@./commit-help.sh

test-commits: ## Test conventional commits setup
	@./test-commits.sh

security-check: ## Run security checks
	bandit -r app/ -c pyproject.toml
	safety check

verify: lint test ## Run all verification checks (lint + test)

ci: install-dev lint test-cov ## CI pipeline: install, lint, and test with coverage
