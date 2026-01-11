.PHONY: help fmt lint typecheck test test-cov test-asyncio run dev-setup docker-build docker-up docker-down clean

help:
	@echo "Python Data Pipeline - Make targets:"
	@echo "  fmt              - Format code with black and isort"
	@echo "  lint             - Run linting (black, isort, flake8)"
	@echo "  typecheck        - Run type checking with mypy"
	@echo "  test             - Run pytest"
	@echo "  test-cov         - Run tests with coverage report"
	@echo "  test-asyncio     - Run async tests with verbose output"
	@echo "  run              - Run pipeline locally (requires DATABASE_URL env var)"
	@echo "  dev-setup        - Setup development environment (venv + deps)"
	@echo "  docker-build     - Build Docker image"
	@echo "  docker-up        - Start Docker Compose stack"
	@echo "  docker-down      - Stop Docker Compose stack"
	@echo "  clean            - Remove build artifacts"

fmt:
	@echo "Formatting code..."
	black src/ tests/
	isort src/ tests/

lint: fmt
	@echo "Running linter..."
	flake8 src/ tests/ --max-line-length=120

typecheck:
	@echo "Running type checker..."
	mypy src/ --ignore-missing-imports

test:
	@echo "Running tests..."
	pytest -v tests/

test-cov:
	@echo "Running tests with coverage..."
	pytest -v --cov=src --cov-report=html --cov-report=term tests/
	@echo "Coverage report: htmlcov/index.html"

test-asyncio:
	@echo "Running async tests with verbose output..."
	pytest -v -s tests/ -k "async"

run:
	@echo "Running pipeline..."
	@if [ -z "$$DATABASE_URL" ]; then \
		echo "Using default SQLite database"; \
		DATABASE_URL="sqlite+aiosqlite:///pipeline.db" \
		CSV_FILE="sample_events.csv" \
		python -m src.main; \
	else \
		CSV_FILE="sample_events.csv" python -m src.main; \
	fi

dev-setup:
	@echo "Setting up development environment..."
	python -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	@echo "Virtual environment created. Activate with: source venv/bin/activate"

docker-build:
	@echo "Building Docker image..."
	docker build -t playbook-pipeline:latest .

docker-up:
	@echo "Starting Docker Compose stack..."
	docker-compose up

docker-down:
	@echo "Stopping Docker Compose stack..."
	docker-compose down

docker-logs:
	@echo "Showing Docker logs..."
	docker-compose logs -f pipeline

docker-clean:
	@echo "Cleaning Docker resources..."
	docker-compose down -v
	docker rmi playbook-pipeline:latest

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov
	rm -rf __pycache__ src/__pycache__ tests/__pycache__
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

.DEFAULT_GOAL := help
