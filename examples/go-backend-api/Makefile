.PHONY: help fmt lint test test-race test-verbose vet run build docker-build docker-up docker-down

help:
	@echo "Go Backend API - Make targets:"
	@echo "  fmt              - Format code with gofmt"
	@echo "  lint             - Run linting (gofmt, go vet)"
	@echo "  vet              - Run go vet"
	@echo "  test             - Run tests with coverage"
	@echo "  test-race        - Run tests with race detector"
	@echo "  test-verbose     - Run tests with verbose output"
	@echo "  run              - Run API locally (requires DATABASE_URL env var)"
	@echo "  build            - Build binary"
	@echo "  docker-build     - Build Docker image"
	@echo "  docker-up        - Start Docker Compose stack"
	@echo "  docker-down      - Stop Docker Compose stack"
	@echo "  clean            - Remove build artifacts"

fmt:
	@echo "Formatting code..."
	gofmt -s -w ./src ./tests

lint: fmt
	@echo "Running linter..."
	go vet ./...

vet:
	@echo "Running go vet..."
	go vet ./...

test:
	@echo "Running tests with coverage..."
	go test -v -cover -coverprofile=coverage.out ./tests/...
	go tool cover -func=coverage.out

test-race:
	@echo "Running tests with race detector..."
	go test -v -race ./tests/...

test-verbose:
	@echo "Running tests with verbose output..."
	go test -v ./tests/...

run:
	@echo "Running API locally..."
	@if [ -z "$$DATABASE_URL" ]; then \
		DATABASE_URL="postgres://postgres:postgres@localhost:5432/playbook_db?sslmode=disable" \
		go run src/main.go; \
	else \
		go run src/main.go; \
	fi

build:
	@echo "Building binary..."
	CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o api src/main.go

docker-build:
	@echo "Building Docker image..."
	docker build -t playbook-api:latest .

docker-up:
	@echo "Starting Docker Compose stack..."
	docker-compose up -d
	@echo "API available at http://localhost:8080"
	@echo "Database: localhost:5432 (postgres/postgres)"

docker-down:
	@echo "Stopping Docker Compose stack..."
	docker-compose down

docker-logs:
	@echo "Showing Docker logs..."
	docker-compose logs -f

clean:
	@echo "Cleaning build artifacts..."
	rm -f api coverage.out coverage.html
	go clean -testcache

.DEFAULT_GOAL := help
