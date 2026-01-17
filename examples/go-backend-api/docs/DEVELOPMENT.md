# Development Guide

How to develop on this Go backend API using the Playbook patterns.

---

## Setup

### Prerequisites
- Go 1.21+
- Docker & Docker Compose (for local development)
- PostgreSQL 15 (if running without Docker)

### Initial Setup

```bash
# 1. Clone and navigate
cd examples/go-backend-api

# 2. Install dependencies
go mod download

# 3. Start PostgreSQL with Docker Compose
docker-compose up postgres

# 4. In another terminal, run the API
export DATABASE_URL="postgres://postgres:postgres@localhost:5432/playbook_db?sslmode=disable"
go run src/main.go
```

Alternatively, start everything:
```bash
docker-compose up
# API runs on http://localhost:8080
```

---

## Development Workflow

Follow the `/pb-start` and `/pb-cycle` pattern:

### 1. Start Work

```bash
# Create feature branch (following /pb-start pattern)
git checkout -b feature/v1.0.0-add-user-filtering main

# Verify setup
go mod download
make test
```

### 2. Develop

Make changes to:
- `src/main.go` — Add handlers, modify business logic
- `tests/handlers_test.go` — Add tests

Example: Add a new endpoint

```go
// In src/main.go, add to setupRoutes():
s.mux.HandleFunc("GET /users/{id}/posts", s.GetUserPosts)

// Implement handler:
func (s *Server) GetUserPosts(w http.ResponseWriter, r *http.Request) {
    // Implementation...
}
```

### 3. Self-Review (Using `/pb-cycle`)

Before committing, check:

```bash
# Format code
make fmt

# Check for lint issues
make lint

# Run tests
make test

# Check race conditions (important for Go)
make test-race

# Quick check: does it build?
go build -o api src/main.go
```

### 4. Commit

```bash
# Logical, atomic commit
git add src/main.go tests/handlers_test.go

git commit -m "feat(users): add user filtering by email"
```

Use this format:
```
<type>(<scope>): <subject>

<body>

- Specific changes made
- Why the change was needed
```

### 5. Peer Review (Using `/pb-cycle`)

Push to GitHub and create PR:
```bash
git push origin feature/v1.0.0-add-user-filtering
# Then use /pb-pr command to create PR
```

Review checklist (from `/pb-guide-go`):
- [ ] gofmt applied (no formatting issues)
- [ ] go vet passes (no warnings)
- [ ] go test -race passes (no race conditions)
- [ ] Test coverage maintained (>70%)
- [ ] Error handling explicit
- [ ] Context used for cancellation
- [ ] Interfaces define contracts
- [ ] No goroutine leaks
- [ ] SQL is parameterized (no injection risks)

---

## Testing

### Run Tests

```bash
# Run all tests
make test

# Run with coverage report
go test -v -cover ./tests/...

# Run with race detector (important!)
make test-race

# Specific test
go test -v -run TestCreateUser ./tests/...
```

### Write Tests

Use table-driven tests (Go idiom):

```go
func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name    string
        email   string
        wantErr bool
    }{
        {"valid", "user@example.com", false},
        {"invalid", "not-an-email", true},
        {"empty", "", true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := validateEmail(tt.email)
            if (err != nil) != tt.wantErr {
                t.Errorf("validateEmail() error = %v, want %v", err, tt.wantErr)
            }
        })
    }
}
```

### Test Database

Tests use PostgreSQL container. Make sure it's running:
```bash
docker-compose up postgres
```

---

## Common Tasks

### Add a New Endpoint

1. **Add handler in `src/main.go`:**

```go
func (s *Server) GetUserByEmail(w http.ResponseWriter, r *http.Request) {
    email := r.URL.Query().Get("email")
    if email == "" {
        http.Error(w, "Email required", http.StatusBadRequest)
        return
    }

    var u User
    err := s.db.QueryRowContext(r.Context(),
        "SELECT id, name, email FROM users WHERE email = $1",
        email,
    ).Scan(&u.ID, &u.Name, &u.Email)

    if err == sql.ErrNoRows {
        http.Error(w, "User not found", http.StatusNotFound)
        return
    }
    if err != nil {
        http.Error(w, "Database error", http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(u)
}
```

2. **Register route in `setupRoutes()`:**

```go
func (s *Server) setupRoutes() {
    // ... existing routes ...
    s.mux.HandleFunc("GET /users/email", s.GetUserByEmail)
}
```

3. **Add test in `tests/handlers_test.go`:**

```go
func TestGetUserByEmail_Success(t *testing.T) {
    db := setupTestDB(t)
    defer db.Close()

    _, err := db.Exec(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        "Alice", "alice@example.com",
    )
    require.NoError(t, err)

    // Test endpoint returns user
    // ...
}
```

4. **Test and commit:**

```bash
make test
git add src/main.go tests/handlers_test.go
git commit -m "feat(users): add GetUserByEmail endpoint"
```

### Modify Database Schema

Edit `initDB()` in `src/main.go`:

```go
schema := `
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20),                         -- NEW
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- NEW
);
`
```

### Add Logging

Use structured logging (from `/pb-patterns-security`):

```go
log.Printf("User created: user_id=%d, email=%s", u.ID, u.Email)

// Or with context
log.Printf("Failed to query user: id=%d, error=%v", id, err)
```

---

## Debugging

### View Logs

```bash
# If running with docker-compose
docker-compose logs -f api

# If running locally, logs appear in stdout
```

### Database Inspection

```bash
# Connect to PostgreSQL
psql playbook_db

# Show users table
SELECT * FROM users;

# Count users
SELECT COUNT(*) FROM users;
```

### API Testing

```bash
# List users
curl http://localhost:8080/users | jq

# Create user
curl -X POST http://localhost:8080/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com"}' | jq

# Get user by ID
curl http://localhost:8080/users/1 | jq

# Delete user
curl -X DELETE http://localhost:8080/users/1
```

---

## Code Quality Gates

Before every commit, check:

```bash
# 1. Format
make fmt

# 2. Lint
make lint

# 3. Test
make test

# 4. Race detector
make test-race

# 5. Build
go build -o api src/main.go
```

Never skip these gates. They catch bugs early.

---

## Performance Testing

### Profile CPU Usage

```bash
# Build with profiling
go build -o api src/main.go

# Import pprof in src/main.go:
import _ "net/http/pprof"

# Access profiles:
go tool pprof http://localhost:8080/debug/pprof/profile

# Check goroutines
curl http://localhost:8080/debug/pprof/goroutine?debug=1
```

### Benchmark

```go
func BenchmarkGetUser(b *testing.B) {
    db := setupTestDB(nil)
    defer db.Close()

    for i := 0; i < b.N; i++ {
        // Benchmark code
    }
}

# Run benchmark
go test -bench=. -benchmem ./tests/...
```

---

## Troubleshooting

### "Connection refused" on database

```bash
# Check if PostgreSQL is running
docker-compose ps

# Start if needed
docker-compose up postgres -d

# Check logs
docker-compose logs postgres
```

### Tests fail with race detector

Use `-race` flag to identify races:
```bash
go test -race -v ./tests/...
```

Fix by:
- Using mutexes for shared data
- Using channels for goroutine coordination
- Avoiding global state

### Build fails

```bash
# Clean and rebuild
go clean -cache
go mod download
go build -o api src/main.go
```

---

## Integration with Playbook

This development workflow follows:
- `/pb-start` — Branch creation, initial setup
- `/pb-cycle` — Develop → Self-review → Test → Commit
- `/pb-guide-go` — Go-specific patterns and tools
- `/pb-testing` — Testing strategy
- `/pb-review-cleanup` — Code review checklist

---

*For more details, see parent `README.md` or Playbook commands.*
