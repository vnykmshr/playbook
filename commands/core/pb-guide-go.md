# Go SDLC Playbook

Language-specific guide for Go projects. Use alongside `/pb-guide` for general process.

**Principle:** Language-specific guidance still assumes `/pb-preamble` thinking (challenge idioms if they don't fit) and applies `/pb-design-rules` thinking throughout.

**Design Rules Applied Here:**
- **Clarity**: Go code should be obvious to readers; favor simplicity over cleverness
- **Simplicity**: Goroutines and channels are powerful but complex; use only what you need
- **Robustness**: Error handling must be explicit; systems should fail loudly, not silently
- **Modularity**: Interfaces and dependency injection enable testability and clear boundaries
- **Optimization**: Profile before optimizing; measure Go programs with `go test -bench` and pprof

Adapt this guide to your project—it's a starting point, not dogma.

---

## **Go-Specific Change Tiers**

Adapt tier based on Go complexity:

| Tier | Examples | Key Considerations |
|------|----------|-------------------|
| **XS** | Typo, vendoring update, simple constant | Format check: `gofmt` |
| **S** | Bug in single handler, dependency update | Test one package: `go test ./handler` |
| **M** | New API endpoint, service refactor | Test full service: `go test ./...` + `go vet` |
| **L** | New service, goroutine patterns | Race detector: `go test -race ./...` |

---

## **Go Project Structure**

Standard Go project layout:

```
myproject/
├── cmd/
│   ├── server/
│   │   └── main.go              # API/Service entry point
│   └── cli/
│       └── main.go              # CLI tool
├── pkg/
│   ├── api/                     # HTTP handlers
│   ├── service/                 # Business logic
│   ├── repository/              # Data access
│   ├── model/                   # Data structures
│   └── config/                  # Configuration
├── internal/
│   ├── middleware/              # HTTP middleware
│   └── utils/                   # Internal helpers
├── go.mod                       # Dependencies
├── go.sum                       # Dependency checksums
├── Dockerfile                   # Container image
├── Makefile                     # Build targets
└── README.md
```

---

## **1. Intake & Clarification (Go-Specific)**

### **1.1 Go-Specific Requirements Restatement**

Document performance and concurrency expectations:
- **Concurrency model:** goroutines, channels, mutex, or single-threaded?
- **Performance budget:** latency targets, throughput, CPU/memory limits
- **Resource constraints:** number of connections, open file descriptors
- **Graceful shutdown:** timeout for in-flight requests

### **1.2 Go Dependency Check**

Before starting:
```bash
go mod tidy          # Remove unused dependencies
go mod verify        # Check integrity
go list -u -m all    # Check for updates
```

---

## **2. Stakeholder Alignment**

### **2.1 Infrastructure & Ops**

Ensure agreement on:
- **Deployment:** Single binary or containers?
- **Database drivers:** PostgreSQL, MySQL, MongoDB?
- **Observability:** Structured logging format, metrics library (Prometheus)
- **Graceful shutdown:** How long to wait for in-flight requests?

### **2.2 Performance Expectations**

Discuss with stakeholders:
```
Latency: <100ms for typical requests
Throughput: X requests/second
Memory: <500MB baseline
Goroutines: <1000 concurrent
```

---

## **3. Go-Specific Requirements Definition**

### **3.1 Concurrency Model**

Define how requests will be handled:

**In-Scope Example:**
- Concurrent requests handled via goroutines
- HTTP handlers parse request, call service, return response
- Background jobs run in separate goroutine pool
- Graceful shutdown waits 30 seconds for in-flight requests

**Out-of-Scope Example:**
- Don't add new database connection pools
- Don't change logging format (already defined)
- Don't modify config loading (use existing pattern)

### **3.2 Dependencies**

List required packages:
```go
// HTTP routing
go get github.com/gorilla/mux

// Database
go get github.com/lib/pq          // PostgreSQL
go get github.com/jmoiron/sqlx     // Query builder

// Logging
go get github.com/sirupsen/logrus

// Testing
go get github.com/stretchr/testify/assert
go get github.com/stretchr/testify/require
```

### **3.3 Goroutine & Channel Usage**

Define patterns:

```
Pattern 1: Request-per-handler (standard)
  GET /api/users/{id} → Handler goroutine → Service → Response

Pattern 2: Background jobs
  Handler queues → Worker pool (5 goroutines) → Process → Log result

Pattern 3: Streaming/SSE
  Client connects → Server sends events → Client closes
```

---

## **4. Go Architecture & Design**

### **4.1 Standard Go Architecture**

```
HTTP Request
    ↓
API Handler (cmd/server/main.go)
    ↓
Middleware (auth, logging, metrics)
    ↓
Service Layer (pkg/service)
    ↓
Repository Layer (pkg/repository)
    ↓
Database
```

### **4.2 Concurrency Pattern**

**For typical web service:**

```go
// Option 1: Goroutines per request (HTTP server does this automatically)
func (h *UserHandler) GetUser(w http.ResponseWriter, r *http.Request) {
    // Handler runs in its own goroutine
    // Parallel requests run concurrently
    userID := r.PathValue("id")
    user, err := h.service.GetUser(r.Context(), userID)
    json.NewEncoder(w).Encode(user)
}

// Option 2: Background job processing
type JobQueue struct {
    queue chan Job
}

func (jq *JobQueue) Start(ctx context.Context) {
    for i := 0; i < 5; i++ {
        go jq.worker(ctx)  // 5 worker goroutines
    }
}

func (jq *JobQueue) worker(ctx context.Context) {
    for {
        select {
        case job := <-jq.queue:
            processJob(job)
        case <-ctx.Done():
            return
        }
    }
}

// Option 3: Context-based cancellation
func (s *UserService) GetUserWithTimeout(ctx context.Context, userID string) (*User, error) {
    // Create timeout context
    ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()

    // Database query respects timeout
    return s.repo.GetUser(ctx, userID)
}
```

### **4.3 Error Handling Pattern**

```go
// [YES] Explicit error handling
func (h *UserHandler) GetUser(w http.ResponseWriter, r *http.Request) {
    userID := r.PathValue("id")
    user, err := h.service.GetUser(r.Context(), userID)
    if err != nil {
        // Specific error handling
        if errors.Is(err, ErrNotFound) {
            http.Error(w, "User not found", http.StatusNotFound)
            return
        }
        http.Error(w, "Internal error", http.StatusInternalServerError)
        return
    }
    json.NewEncoder(w).Encode(user)
}

// [NO] Ignoring errors
func (h *UserHandler) GetUser(w http.ResponseWriter, r *http.Request) {
    user, _ := h.service.GetUser(r.Context(), userID)  // Error ignored!
    json.NewEncoder(w).Encode(user)
}
```

### **4.4 Interface-Driven Design**

```go
// Define interfaces for testability
type UserRepository interface {
    GetUser(ctx context.Context, id string) (*User, error)
    CreateUser(ctx context.Context, user *User) (*User, error)
}

type UserService interface {
    GetUser(ctx context.Context, id string) (*User, error)
}

// Implement with real database
type PostgresUserRepository struct {
    db *sqlx.DB
}

// Implement with mock for testing
type MockUserRepository struct {
    GetUserFunc func(ctx context.Context, id string) (*User, error)
}
```

---

## **5. Implementation (Go-Specific)**

### **5.1 Code Quality Tools**

Required for all commits:

```bash
# Format code (enforced)
gofmt -s -w ./...
go mod tidy

# Lint code
go vet ./...
golangci-lint run ./...  # If using

# Unit tests (S, M, L tiers)
go test -v -race -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

### **5.2 Testing Patterns**

**Unit Test Structure:**
```go
package service_test

import (
    "context"
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestGetUser_Success(t *testing.T) {
    // Arrange
    mockRepo := &MockUserRepository{
        GetUserFunc: func(ctx context.Context, id string) (*User, error) {
            return &User{ID: id, Name: "John"}, nil
        },
    }
    service := NewUserService(mockRepo)

    // Act
    user, err := service.GetUser(context.Background(), "123")

    // Assert
    require.NoError(t, err)
    assert.Equal(t, "John", user.Name)
}

func TestGetUser_NotFound(t *testing.T) {
    mockRepo := &MockUserRepository{
        GetUserFunc: func(ctx context.Context, id string) (*User, error) {
            return nil, ErrNotFound
        },
    }
    service := NewUserService(mockRepo)

    user, err := service.GetUser(context.Background(), "999")

    assert.Nil(t, user)
    assert.Equal(t, ErrNotFound, err)
}
```

**Integration Test:**
```go
func TestGetUserIntegration(t *testing.T) {
    // Use actual database or test container
    db := setupTestDB(t)
    defer db.Close()

    repo := NewPostgresUserRepository(db)
    service := NewUserService(repo)

    user, err := service.GetUser(context.Background(), "real_user_id")

    require.NoError(t, err)
    assert.NotNil(t, user)
}
```

### **5.3 Goroutine Best Practices**

```go
// [YES] Use WaitGroup for coordinating goroutines
func fetchDataConcurrently(ctx context.Context, userIDs []string) ([]User, error) {
    var wg sync.WaitGroup
    users := make([]User, len(userIDs))
    errors := make([]error, len(userIDs))

    for i, id := range userIDs {
        wg.Add(1)
        go func(idx int, userID string) {
            defer wg.Done()
            user, err := getUser(ctx, userID)
            users[idx] = user
            errors[idx] = err
        }(i, id)
    }

    wg.Wait()

    for _, err := range errors {
        if err != nil {
            return nil, err
        }
    }

    return users, nil
}

// [YES] Use context for cancellation
func (s *Service) ProcessRequest(ctx context.Context) error {
    done := make(chan error)

    go func() {
        done <- s.longRunningTask()
    }()

    select {
    case err := <-done:
        return err
    case <-ctx.Done():
        // Parent cancelled, clean up and return
        return ctx.Err()
    }
}

// [NO] Goroutine without way to stop
go func() {
    for {
        // Infinite loop, can't be cancelled
        doWork()
    }
}()
```

### **5.4 Database Patterns**

**Connection Pool:**
```go
import "database/sql"

db, err := sql.Open("postgres", "postgres://...")
db.SetMaxOpenConns(25)      // Max concurrent connections
db.SetMaxIdleConns(5)       // Keep idle connections for reuse
db.SetConnMaxLifetime(5*time.Minute)

// All queries use pooling automatically
user, err := db.QueryRow("SELECT * FROM users WHERE id=$1", userID).Scan(&user)
```

**Query Pattern:**
```go
// [YES] Prepared statements prevent SQL injection
stmt, err := db.Prepare("SELECT * FROM users WHERE id = $1")
defer stmt.Close()

row := stmt.QueryRow(userID)
err = row.Scan(&user.ID, &user.Name, &user.Email)

// [NO] String concatenation (SQL injection risk!)
query := "SELECT * FROM users WHERE id = " + userID  // DANGER!
```

**Transaction Pattern:**
```go
func (r *UserRepository) UpdateUser(ctx context.Context, user *User) error {
    tx, err := r.db.BeginTx(ctx, nil)
    if err != nil {
        return err
    }
    defer tx.Rollback()

    // Update user
    _, err = tx.ExecContext(ctx,
        "UPDATE users SET name=$1, email=$2 WHERE id=$3",
        user.Name, user.Email, user.ID)
    if err != nil {
        return err
    }

    // Update related data
    _, err = tx.ExecContext(ctx,
        "UPDATE user_profiles SET updated_at=NOW() WHERE user_id=$1",
        user.ID)
    if err != nil {
        return err
    }

    return tx.Commit().Err()
}
```

---

## **6. Testing Readiness (Go-Specific)**

### **6.1 Test Coverage Requirements**

| Tier | Coverage | Command |
|------|----------|---------|
| **S** | >50% | `go test -cover ./...` |
| **M** | >70% | `go test -cover -race ./...` |
| **L** | >80% | `go test -cover -race ./...` |

```bash
# Generate coverage report
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out

# Run with race detector (M, L tiers)
go test -race ./...
```

### **6.2 Test Patterns**

**Table-Driven Tests (Go idiom):**
```go
func TestUserValidation(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    bool
        wantErr bool
    }{
        {"valid email", "test@example.com", true, false},
        {"invalid email", "not-an-email", false, true},
        {"empty", "", false, true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := ValidateEmail(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("ValidateEmail() error = %v, wantErr %v", err, tt.wantErr)
            }
            if got != tt.want {
                t.Errorf("ValidateEmail() = %v, want %v", got, tt.want)
            }
        })
    }
}
```

**Subtests:**
```go
func TestUserService(t *testing.T) {
    t.Run("GetUser", func(t *testing.T) {
        // Subtest for GetUser
    })

    t.Run("CreateUser", func(t *testing.T) {
        // Subtest for CreateUser
    })
}
```

---

## **7. Code Review Checklist (Go-Specific)**

Before PR review:

- [ ] `go fmt` applied (no formatting changes in review)
- [ ] `go vet ./...` passes (no warnings)
- [ ] `go test -race ./...` passes (no race conditions)
- [ ] Test coverage maintained/improved (>70%)
- [ ] Error handling explicit (no ignored errors)
- [ ] Context used for cancellation (not timeout parameters)
- [ ] Interfaces define contracts (for testability)
- [ ] No goroutine leaks (all goroutines can be stopped)
- [ ] Deadlock-free (proper channel usage)
- [ ] Dependencies vendored/managed (go.mod/go.sum)

---

## **8. Deployment (Go-Specific)**

### **8.1 Build Artifacts**

```bash
# Build static binary
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o server cmd/server/main.go

# Build with version info
go build -ldflags "-X main.Version=1.0.0 -X main.Build=$(git rev-parse --short HEAD)" \
  -o server cmd/server/main.go
```

### **8.2 Container Image**

```dockerfile
# Multi-stage build
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 go build -o server cmd/server/main.go

FROM alpine:latest
RUN apk --no-cache add ca-certificates  # For HTTPS
COPY --from=builder /app/server /server
EXPOSE 8080
ENTRYPOINT ["/server"]
```

### **8.3 Graceful Shutdown**

```go
func main() {
    server := &http.Server{
        Addr:    ":8080",
        Handler: router,
    }

    // Handle shutdown signals
    sigChan := make(chan os.Signal, 1)
    signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)

    go func() {
        <-sigChan
        // Graceful shutdown: wait 30 seconds for requests to finish
        ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
        defer cancel()

        if err := server.Shutdown(ctx); err != nil {
            log.Fatalf("Server shutdown failed: %v", err)
        }
    }()

    log.Fatal(server.ListenAndServe())
}
```

---

## **9. Observability (Go-Specific)**

### **9.1 Structured Logging**

```go
import "github.com/sirupsen/logrus"

log := logrus.New()
log.SetFormatter(&logrus.JSONFormatter{})

// Log with context
log.WithFields(logrus.Fields{
    "user_id": userID,
    "action":  "user.created",
    "duration": 150,  // milliseconds
}).Info("User created successfully")

// Error logging with stack trace
log.WithError(err).Error("Failed to get user")
```

### **9.2 Metrics (Prometheus)**

```go
import "github.com/prometheus/client_golang/prometheus"

// Counter for requests
var httpRequests = prometheus.NewCounterVec(
    prometheus.CounterOpts{Name: "http_requests_total"},
    []string{"method", "path", "status"},
)

// Histogram for latency
var httpDuration = prometheus.NewHistogramVec(
    prometheus.HistogramOpts{Name: "http_request_duration_seconds"},
    []string{"method", "path"},
)

// In handler
start := time.Now()
httpRequests.WithLabelValues(r.Method, r.URL.Path, "200").Inc()
httpDuration.WithLabelValues(r.Method, r.URL.Path).Observe(time.Since(start).Seconds())
```

### **9.3 Profiling**

```go
import _ "net/http/pprof"

// Enable profiling endpoint
go func() {
    log.Println(http.ListenAndServe("localhost:6060", nil))
}()

// Access profiles:
// CPU:    go tool pprof http://localhost:6060/debug/pprof/profile
// Memory: go tool pprof http://localhost:6060/debug/pprof/heap
```

---

## **10. Release & Post-Release**

### **10.1 Release Checklist**

- [ ] All tests pass: `go test -race ./...`
- [ ] Coverage >70%: `go test -coverprofile=coverage.out ./...`
- [ ] Dependencies up-to-date: `go mod tidy && go mod verify`
- [ ] Git tag created: `git tag v1.2.3`
- [ ] Docker image built and pushed
- [ ] Rollback plan documented
- [ ] Monitoring alerts configured

### **10.2 Rollback**

If deployed version has issues:

```bash
# Revert to previous tag
git checkout v1.2.2
CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o server cmd/server/main.go
# Deploy previous binary
```

### **10.3 Post-Release Monitoring**

Monitor for:
- Error rates (logs, Prometheus)
- Goroutine count (should be stable)
- Memory usage (shouldn't grow unbounded)
- Latency (p50, p95, p99)

```bash
# Check goroutines
curl localhost:6060/debug/pprof/goroutine?debug=1

# Check memory
go tool pprof http://localhost:6060/debug/pprof/heap
```

---

## **Integration with Playbook**

**Related Commands:**
- `/pb-guide` — General SDLC process
- `/pb-patterns-core` — Architectural patterns
- `/pb-patterns-async` — Concurrency patterns
- `/pb-performance` — Performance optimization
- `/pb-testing` — Advanced testing strategies
- `/pb-deployment` — Deployment and DevOps

---

*Created: 2026-01-11 | Category: Language Guides | Language: Go | Tier: L*
