# Go Backend API Example

A minimal but realistic Go REST API demonstrating how to use the Engineering Playbook (`/pb-*` commands) in a real project.

---

## What This Project Does

Simple REST API for managing users:
- **GET /users** — List all users
- **GET /users/{id}** — Get single user
- **POST /users** — Create user
- **DELETE /users/{id}** — Delete user

Data stored in PostgreSQL. Includes connection pooling, graceful shutdown, and structured error handling.

---

## How This Project Uses the Playbook

### Planning Phase
- **`/pb-plan`** — Define scope (API endpoints, database schema, error handling)
- **`/pb-adr`** — Decisions: why PostgreSQL, connection pool settings, error strategy

### Development
- **`/pb-start`** — Create feature branch, establish development rhythm
- **`/pb-cycle`** — Each API endpoint: develop → self-review → test → commit
- **`/pb-guide-go`** — Language-specific patterns: goroutines, channels, error handling

### Testing
- **`/pb-testing`** — Unit tests (handlers), integration tests (with database)
- Run: `make test` (uses `/pb-testing` approach)

### Code Quality
- **`/pb-standards`** — Code formatting, error handling patterns
- Run: `make lint` (gofmt, go vet)

### Security
- **`/pb-patterns-security`** — Input validation, SQL injection prevention
- **`/pb-security`** — Security checklist before release

### Code Review
- **`/pb-cycle`** — Peer review each commit
- **`/pb-review-hygiene`** — Multi-perspective review (testing, performance, security)

### Release & Deployment
- **`/pb-release`** — Pre-release checks, smoke tests
- **`/pb-deployment`** — Container deployment, rollback strategy
- **`/pb-patterns-core`** — Circuit breaker, retry patterns for client calls

---

## Quick Start

### Prerequisites
- Go 1.21+
- Docker & Docker Compose
- Make (optional, for Makefile)

### 1. Run Locally with Docker Compose

```bash
cd examples/go-backend-api

# Start API and PostgreSQL
docker-compose up

# In another terminal, test the API
curl http://localhost:8080/users

# Create user
curl -X POST http://localhost:8080/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com"}'

# Stop
docker-compose down
```

### 2. Develop Locally (Without Docker)

**Prerequisites:**
```bash
# Install Go (1.21+)
brew install go  # macOS

# Install PostgreSQL
brew install postgresql@15  # macOS

# Start PostgreSQL locally
brew services start postgresql@15
```

**Setup:**
```bash
cd examples/go-backend-api

# Create database
createdb playbook_db

# Download dependencies
go mod download

# Run tests
go test -v -race ./...

# Run application
export DATABASE_URL="postgres://$(whoami)@localhost/playbook_db?sslmode=disable"
go run src/main.go
```

### 3. Use Playbook Commands

#### Start a new feature
```bash
# From /pb-start
git checkout -b feature/v1.0.0-user-filtering main

# Make changes
# Run /pb-cycle for each iteration
```

#### Run tests and linting
```bash
make test         # Tests + coverage
make lint         # gofmt + go vet
make run          # Run locally
```

#### Review code
```bash
# Use /pb-cycle at each iteration
# Use /pb-review-hygiene for final review
```

#### Create PR
```bash
git push origin feature/v1.0.0-user-filtering
# Use /pb-pr to create PR with proper context
```

---

## Project Structure

```
go-backend-api/
├── src/
│   └── main.go              Main application (API server, database)
├── tests/
│   └── handlers_test.go     Unit tests for HTTP handlers
├── docs/
│   ├── DEVELOPMENT.md       Development workflow
│   ├── ARCHITECTURE.md      System design, API specs
│   ├── TESTING.md           Testing strategy
│   ├── SECURITY.md          Security checklist
│   └── CODE-REVIEW.md       Code review process
├── .github/workflows/
│   └── ci.yml               GitHub Actions CI/CD
├── docker-compose.yml       Local development stack
├── Dockerfile               Container image
├── Makefile                 Build targets
├── go.mod                   Go module definition
└── README.md                This file
```

---

## Key Patterns from Playbook

### 1. Connection Pooling (`/pb-patterns-db`)
```go
db.SetMaxOpenConns(25)      // From pb-guide-go patterns
db.SetMaxIdleConns(5)
db.SetConnMaxLifetime(5 * time.Minute)
```

### 2. Graceful Shutdown (`/pb-guide-go`)
```go
sigChan := make(chan os.Signal, 1)
signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)
// Server waits 30s for in-flight requests before shutdown
```

### 3. Error Handling (`/pb-patterns-core` + `/pb-guide-go`)
- Explicit error checking (not silent failures)
- Structured logging with context
- HTTP status codes match error types

### 4. Testing (`/pb-testing` + `/pb-guide-go`)
- Table-driven tests for input validation
- Integration tests with real database
- Run with race detector: `go test -race ./...`

### 5. Security (`/pb-security` + `/pb-patterns-security`)
- Input validation before database queries
- Parameterized queries (prevent SQL injection)
- No hardcoded secrets (use environment variables)

---

## How to Adapt This Project

### Fork It
```bash
cp -r examples/go-backend-api /path/to/my-project
cd /path/to/my-project
go mod edit -module github.com/myorg/my-api
```

### Customize
1. Replace database schema in `src/main.go` → `initDB()`
2. Add new HTTP handlers following `GetUser` pattern
3. Add tests for new handlers in `tests/handlers_test.go`
4. Update docs with your specific architecture

### Use Playbook Commands
- `/pb-plan` — Plan your features
- `/pb-start` → `/pb-cycle` — Development iteration
- `/pb-testing` — Test strategy
- `/pb-release` — Release checklist

---

## Development Workflow

### Create a Feature

```bash
# Step 1: Plan (using /pb-plan)
# Define: scope, acceptance criteria, dependencies

# Step 2: Start development (using /pb-start)
git checkout -b feature/v1.0.0-new-endpoint main

# Step 3: Each iteration (using /pb-cycle)
# - Write code
# - Self-review
# - Test (make test)
# - Commit (git commit with clear message)

# Step 4: Final review (using /pb-review-hygiene)
# - Security perspective (pb-security checklist)
# - Testing perspective (pb-testing coverage)
# - Performance perspective (pb-performance profiling)

# Step 5: Release (using /pb-release)
# - Pre-release checks
# - Deploy to staging
# - Smoke tests
# - Tag version: git tag v1.0.0
```

### Run Tests
```bash
make test           # Run all tests with coverage
make test-race      # Run with race detector
make test-verbose   # Detailed output
```

### Code Quality
```bash
make lint           # Format + lint checks
make vet            # Go vet analysis
make fmt            # Format code
```

---

## Integration with CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`):
1. Checkout code
2. Setup Go
3. Download dependencies
4. Run linting
5. Run tests (with race detector)
6. Build Docker image
7. (Optional) Push to registry

Uses playbook patterns:
- `/pb-guide-go` — Testing & build strategy
- `/pb-deployment` — Container deployment
- `/pb-release` — Release gates

---

## Security Considerations

See `docs/SECURITY.md` for detailed checklist.

Key points:
- ✅ Parameterized queries (no SQL injection)
- ✅ Input validation before database
- ✅ Environment variables for secrets (no hardcoding)
- ✅ CORS headers (if needed)
- ✅ Rate limiting (implement from `/pb-patterns-core`)
- ✅ Structured error logging (no sensitive data)

---

## Related Playbook Commands

- `/pb-guide-go` — Go-specific SDLC guide (concurrency, testing, deployment)
- `/pb-patterns-core` — Core architectural patterns (connection pooling, error handling)
- `/pb-patterns-db` — Database patterns (pooling, optimization, replication)
- `/pb-security` — Security checklist and patterns
- `/pb-testing` — Testing strategy and best practices
- `/pb-deployment` — Deployment and DevOps practices

---

## Support

For questions about:
- **Playbook patterns** → See `/pb-guide` or specific `/pb-*` command
- **Go development** → See `/pb-guide-go`
- **Database patterns** → See `/pb-patterns-db`
- **This example project** → See `docs/DEVELOPMENT.md`

---

*This example is part of the Engineering Playbook project.*
*Last updated: 2026-01-12*
