# Multi-stage build
FROM golang:1.21-alpine AS builder

WORKDIR /build

# Install build dependencies
RUN apk add --no-cache git

# Copy go mod files
COPY go.mod go.sum* ./

# Download dependencies
RUN go mod download

# Copy source code
COPY src/ ./src/
COPY tests/ ./tests/

# Build application
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o api ./src/main.go

# Runtime stage
FROM alpine:latest

# Install runtime dependencies (for database SSL, etc.)
RUN apk --no-cache add ca-certificates

WORKDIR /app

# Copy binary from builder
COPY --from=builder /build/api ./api

# Health check
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

EXPOSE 8080

CMD ["./api"]
