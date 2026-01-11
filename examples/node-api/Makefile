.PHONY: help install build dev test test-watch test-coverage lint lint-fix format typecheck run docker-build docker-up docker-down clean

help:
	@echo "Node.js API - Make targets:"
	@echo "  install          - Install dependencies"
	@echo "  build            - Build TypeScript to JavaScript"
	@echo "  dev              - Run in development mode with hot reload"
	@echo "  test             - Run tests"
	@echo "  test-watch       - Run tests in watch mode"
	@echo "  test-coverage    - Run tests with coverage report"
	@echo "  lint             - Run ESLint"
	@echo "  lint-fix         - Fix ESLint issues"
	@echo "  format           - Format code with Prettier"
	@echo "  typecheck        - Type check with TypeScript"
	@echo "  run              - Run production build"
	@echo "  docker-build     - Build Docker image"
	@echo "  docker-up        - Start Docker Compose stack"
	@echo "  docker-down      - Stop Docker Compose stack"
	@echo "  clean            - Remove build artifacts"

install:
	@echo "Installing dependencies..."
	npm ci

build:
	@echo "Building TypeScript..."
	npm run build

dev:
	@echo "Running in development mode..."
	npm run dev

test:
	@echo "Running tests..."
	npm test

test-watch:
	@echo "Running tests in watch mode..."
	npm run test:watch

test-coverage:
	@echo "Running tests with coverage..."
	npm run test:coverage

lint:
	@echo "Running linter..."
	npm run lint

lint-fix:
	@echo "Fixing linter issues..."
	npm run lint:fix

format:
	@echo "Formatting code..."
	npm run format

typecheck:
	@echo "Type checking..."
	npm run typecheck

run: build
	@echo "Running production build..."
	npm start

docker-build:
	@echo "Building Docker image..."
	docker build -t playbook-node-api:latest .

docker-up:
	@echo "Starting Docker Compose stack..."
	docker-compose up

docker-down:
	@echo "Stopping Docker Compose stack..."
	docker-compose down

docker-logs:
	@echo "Showing Docker logs..."
	docker-compose logs -f api

clean:
	@echo "Cleaning build artifacts..."
	rm -rf dist coverage node_modules
	npm cache clean --force

.DEFAULT_GOAL := help
