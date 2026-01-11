# Playbook in Action: Real-World Examples

This guide demonstrates how development teams use the Engineering Playbook commands in realistic projects. Three complete example projects showcase the playbook patterns across different technology stacks.

---

## Table of Contents

1. [Starting a Feature](#starting-a-feature)
2. [Example Projects](#example-projects)
3. [Development Workflow](#development-workflow)
4. [Code Quality Gates](#code-quality-gates)
5. [Testing & Validation](#testing--validation)
6. [Creating Pull Requests](#creating-pull-requests)
7. [Common Scenarios](#common-scenarios)

---

## Starting a Feature

### Using `/pb-start`

Every new feature begins with creating a feature branch:

```bash
/pb-start
```

This command guides you through:
- Naming your feature branch (e.g., `feature/v1.3.0-user-profiles`)
- Creating it from the main branch
- Configuring your development environment

All three example projects follow this pattern:

| Project | Technology | Start Command |
|---------|-----------|---|
| **Go Backend API** | Go 1.22 | `git checkout -b feature/v1.3.0-new-endpoint main` |
| **Python Pipeline** | Python 3.11 | `git checkout -b feature/v1.3.0-event-aggregation main` |
| **Node.js API** | Node.js 20 + TypeScript | `git checkout -b feature/v1.3.0-user-roles main` |

---

## Example Projects

### 1. Go Backend API

**Location:** `examples/go-backend-api/`

**Purpose:** REST API for managing users, demonstrating Go best practices

**Tech Stack:**
- Go 1.22 with built-in HTTP routing
- PostgreSQL with connection pooling
- Table-driven tests
- Race condition detection

**Quick Start:**

```bash
cd examples/go-backend-api

# Option 1: Docker Compose (Recommended)
docker-compose up

# Option 2: Local development
make install
make dev
```

**API Endpoints:**

```bash
# Health check
GET /health

# List all users
GET /users

# Get single user
GET /users/1

# Create user
POST /users -d '{"name":"Alice","email":"alice@example.com"}'

# Delete user
DELETE /users/1
```

**Playbook Commands Used:**

- `/pb-start` — Create feature branch
- `/pb-cycle` — Develop → test → commit workflow
- `/pb-testing` — Unit tests with table-driven patterns
- `/pb-patterns-core` — Error handling, connection pooling
- `/pb-security` — Parameterized queries, input validation

**Development Workflow:**

```bash
# 1. Start feature
git checkout -b feature/v1.3.0-new-endpoint main

# 2. Create new endpoint
vim src/main.go

# 3. Run locally
make dev

# 4. Write and run tests
make test

# 5. Type checking (Go vet)
make lint

# 6. Commit
make test && git add . && git commit -m "feat: add new endpoint"

# 7. Create PR
/pb-pr
```

---

### 2. Python Data Pipeline

**Location:** `examples/python-data-pipeline/`

**Purpose:** Async data pipeline for processing user events with aggregation

**Tech Stack:**
- Python 3.11 with async/await
- SQLAlchemy async ORM
- Pytest with async fixtures
- Type hints with mypy

**Quick Start:**

```bash
cd examples/python-data-pipeline

# Option 1: Docker Compose
docker-compose up

# Option 2: Local with virtual environment
make dev-setup
source venv/bin/activate
make test
make run
```

**Pipeline Stages:**

```python
# Read events from CSV
events = await pipeline.read_events_from_csv('sample_events.csv')

# Ingest into database
await pipeline.ingest_events(events)

# Process and aggregate
await pipeline.process_events()

# Retrieve summaries
summaries = await pipeline.get_all_summaries()
```

**Playbook Commands Used:**

- `/pb-start` — Create feature branch
- `/pb-cycle` — Develop → test → commit workflow
- `/pb-testing` — Pytest async fixtures and parametrized tests
- `/pb-patterns-core` — Async error handling, type hints
- `/pb-standards` — Black formatting, isort, mypy type checking

**Development Workflow:**

```bash
# 1. Start feature
git checkout -b feature/v1.3.0-event-aggregation main

# 2. Add new pipeline stage
vim src/main.py

# 3. Run locally
make run

# 4. Write async tests
vim tests/test_pipeline.py

# 5. Run tests
make test

# 6. Format and type check
make fmt && make typecheck

# 7. Commit
make test && git add . && git commit -m "feat: add event aggregation"

# 8. Create PR
/pb-pr
```

---

### 3. Node.js REST API

**Location:** `examples/node-api/`

**Purpose:** Express.js REST API with TypeScript for user management

**Tech Stack:**
- Node.js 20 with TypeScript
- Express.js web framework
- PostgreSQL with pg client
- Jest + Supertest for testing
- Pino for structured logging

**Quick Start:**

```bash
cd examples/node-api

# Option 1: Docker Compose
docker-compose up

# Option 2: Local development
make install
make dev
```

**API Endpoints:**

```bash
# Health check
GET /health

# List all users
GET /users

# Get single user
GET /users/1

# Create user
POST /users -d '{"name":"Bob","email":"bob@example.com"}'

# Delete user
DELETE /users/1
```

**Playbook Commands Used:**

- `/pb-start` — Create feature branch
- `/pb-cycle` — Develop → test → commit workflow
- `/pb-testing` — Jest unit and integration tests with Supertest
- `/pb-patterns-core` — Type-safe error handling, request tracing
- `/pb-observability` — Structured logging, request ID tracking

**Development Workflow:**

```bash
# 1. Start feature
git checkout -b feature/v1.3.0-user-roles main

# 2. Add new endpoint
vim src/main.ts

# 3. Add tests
vim tests/api.test.ts

# 4. Run in dev mode
make dev

# 5. Run tests
make test

# 6. Type check and lint
make typecheck && make lint-fix

# 7. Format
make format

# 8. Commit
make test && git add . && git commit -m "feat: add user roles"

# 9. Create PR
/pb-pr
```

---

## Development Workflow

All three projects follow the same development cycle using `/pb-cycle`:

### Step 1: Develop

Write feature code and run locally:

```bash
make dev          # Watch mode with auto-reload
make typecheck    # Type checking
make lint         # Linting
```

### Step 2: Test

Comprehensive test coverage:

```bash
make test              # Run all tests
make test-watch        # Watch mode
make test-coverage     # Coverage report
```

### Step 3: Code Quality

Ensure code meets standards:

```bash
make format       # Auto-format code
make lint-fix     # Auto-fix linting issues
make typecheck    # Type checking
```

### Step 4: Commit

Create atomic, well-documented commits:

```bash
git add .
git commit -m "feat: description of feature"
# Or use /pb-commit for guided commit
```

### Step 5: Repeat

Iterate until feature is complete:

```bash
# Repeat steps 1-4 for each logical change
```

---

## Code Quality Gates

### Pre-Commit Checks

All projects require passing these checks before committing:

```bash
# Go Backend API
make lint    # go vet
make test    # go test with coverage
make test-race  # Race condition detection

# Python Pipeline
make fmt      # black + isort
make lint     # flake8
make typecheck  # mypy
make test     # pytest

# Node.js API
make lint     # eslint
make format   # prettier
make typecheck  # tsc
make test     # jest
```

### Pull Request Checks

CI/CD pipeline runs the same checks automatically. If local checks pass, PR will succeed.

```bash
# Before pushing to PR
make lint && make typecheck && make format && make test
```

### Coverage Requirements

All projects use coverage tracking:

```bash
# Go
make test  # Includes coverage

# Python
make test-cov

# Node.js
make test-coverage
```

---

## Testing & Validation

### Unit Tests

Test individual functions and logic:

**Go Example:**
```go
func TestCreateUser(t *testing.T) {
	// Table-driven test
	tests := []struct {
		name    string
		input   CreateUserInput
		wantErr bool
	}{
		{"valid user", CreateUserInput{...}, false},
		{"invalid email", CreateUserInput{...}, true},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Test logic
		})
	}
}
```

**Python Example:**
```python
@pytest.mark.asyncio
async def test_ingest_events_success(pipeline):
	events = [{'user_id': '1', 'event_type': 'login', 'data': ''}]
	count = await pipeline.ingest_events(events)
	assert count == 1
```

**Node.js Example:**
```typescript
describe('POST /users', () => {
	it('should create user with valid input', async () => {
		const response = await request(app)
			.post('/users')
			.send({ name: 'Alice', email: 'alice@example.com' });
		expect(response.status).toBe(201);
	});
});
```

### Integration Tests

Test full workflows and API flows:

```bash
# All projects include integration tests
make test  # Runs all test types
```

### Docker Validation

All projects validate successfully with Docker Compose:

```bash
# Start the full stack
docker-compose up

# In another terminal, test endpoints
curl http://localhost:3000/health      # Node.js
curl http://localhost:8080/health      # Go
# Python: docker-compose logs api
```

---

## Creating Pull Requests

### Using `/pb-pr`

```bash
/pb-pr
```

This guides you through:

1. **Title:** Clear, descriptive title for the feature
2. **Summary:** 2-3 bullet points explaining what changed
3. **Test Plan:** Checklist of what to test
4. **Labels:** Tag with type (feature, bugfix, docs, etc.)

### Example PR Description

```markdown
## Summary

- Added user profile endpoints (GET /users/:id/profile, PATCH /users/:id/profile)
- Implemented type-safe request/response validation
- Added request ID tracking for distributed tracing

## Test Plan

- [x] Unit tests pass locally (`make test`)
- [x] Integration tests validate endpoints
- [x] Type checking passes (`make typecheck`)
- [x] Code follows standards (`make lint && make format`)
- [x] Tested with Postman/curl

## Notes

This feature demonstrates:
- `/pb-testing` - Comprehensive test coverage
- `/pb-patterns-core` - Type-safe error handling
- `/pb-observability` - Request tracing
```

---

## Common Scenarios

### Scenario 1: Adding a New API Endpoint

**Go Example:**

```bash
# 1. Start feature
git checkout -b feature/v1.3.0-posts-endpoint main

# 2. Add handler
vim src/main.go
# Add GetUserPosts handler and register route

# 3. Write tests
vim tests/handlers_test.go

# 4. Run and test
make dev
curl http://localhost:8080/users/1/posts

# 5. Ensure quality
make test && make lint && make test-race

# 6. Commit
git commit -m "feat: add user posts endpoint"

# 7. Push and PR
git push origin feature/v1.3.0-posts-endpoint
/pb-pr
```

### Scenario 2: Adding a Pipeline Stage

**Python Example:**

```bash
# 1. Start feature
git checkout -b feature/v1.3.0-anomaly-detection main

# 2. Add new method to Pipeline class
vim src/main.py
# def detect_anomalies(self) -> List[dict]:

# 3. Write async tests
vim tests/test_pipeline.py

# 4. Run tests locally
make test

# 5. Format and type check
make fmt && make typecheck

# 6. Commit
git commit -m "feat: add anomaly detection to pipeline"

# 7. Push and PR
git push origin feature/v1.3.0-anomaly-detection
/pb-pr
```

### Scenario 3: Fixing a Bug with Tests

**Node.js Example:**

```bash
# 1. Create feature branch
git checkout -b bugfix/v1.3.0-email-validation main

# 2. Write a failing test for the bug
vim tests/api.test.ts
# Add test that reproduces the issue

# 3. Verify test fails
make test

# 4. Fix the code
vim src/main.ts

# 5. Verify test passes
make test

# 6. Ensure no regressions
make test-coverage

# 7. Commit with explanation
git commit -m "fix: improve email validation

- Add regex check for valid email format
- Reject emails without domain
- Add test case to prevent regression"

# 8. Push and PR
git push origin bugfix/v1.3.0-email-validation
/pb-pr
```

### Scenario 4: Code Review Feedback

When reviewer asks for changes:

```bash
# 1. Pull latest feedback
git pull

# 2. Make changes
vim src/main.ts

# 3. Verify tests still pass
make test && make typecheck

# 4. Commit additional changes
git commit -m "review: address feedback on error handling"

# 5. Push (auto-updates PR)
git push origin feature/branch-name
```

---

## Key Takeaways

### Universal Patterns

All three example projects demonstrate:

1. **Type Safety** — Go generics, Python type hints, TypeScript
2. **Error Handling** — Structured error responses with status codes
3. **Testing** — Unit and integration tests with good coverage
4. **Code Quality** — Linting, formatting, type checking
5. **Database Access** — Connection pooling, parameterized queries
6. **Structured Logging** — Context-aware, tracing-friendly logs
7. **Docker Ready** — Multi-stage builds, health checks
8. **Graceful Shutdown** — Signal handling, timeout management

### Playbook Command Usage

| Scenario | Command | Purpose |
|----------|---------|---------|
| Start new feature | `/pb-start` | Create feature branch |
| Development cycle | `/pb-cycle` | Develop → test → commit |
| Testing | `/pb-testing` | Test strategy and patterns |
| Code standards | `/pb-standards` | Formatting and linting |
| Error handling | `/pb-patterns-core` | Design patterns |
| Security | `/pb-security` | Input validation, injection prevention |
| Create PR | `/pb-pr` | Submit work for review |
| Commit message | `/pb-commit` | Write atomic commits |

---

## Running the Examples

To run all three examples locally:

```bash
# Go Backend API (Port 8080)
cd examples/go-backend-api && docker-compose up &

# Python Pipeline (Runs once, exits)
cd examples/python-data-pipeline && docker-compose up &

# Node.js API (Port 3000)
cd examples/node-api && docker-compose up &

# Test endpoints
curl http://localhost:8080/health    # Go
curl http://localhost:3000/health    # Node.js
docker-compose logs api              # Python (check logs)
```

---

## Next Steps

1. **Choose your stack** — Pick the technology that matches your team
2. **Copy the example** — Use as template for your project
3. **Customize** — Adapt to your specific needs
4. **Use the playbook** — Apply `/pb-*` commands to your workflow
5. **Iterate** — Follow the development cycle documented here

For more details on each example:

- **Go Backend:** `examples/go-backend-api/docs/DEVELOPMENT.md`
- **Python Pipeline:** `examples/python-data-pipeline/docs/DEVELOPMENT.md`
- **Node.js API:** `examples/node-api/docs/DEVELOPMENT.md`

---

*This guide demonstrates the Engineering Playbook in action across three realistic projects.*
*Last updated: 2026-01-12*
