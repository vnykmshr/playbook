# Python Data Pipeline Example

A minimal but realistic Python data processing pipeline demonstrating how to use the Engineering Playbook (`/pb-*` commands) in a batch processing context.

---

## What This Project Does

Async data pipeline for processing user events:
- **Read CSV** — Load events from CSV file
- **Ingest** — Store events in PostgreSQL with validation
- **Process** — Generate user event summaries
- **Report** — Display aggregated statistics

Features:
- Async/await with SQLAlchemy async ORM
- Structured logging with context
- Database transactions with rollback
- Comprehensive error handling
- Type hints throughout

---

## How This Project Uses the Playbook

### Planning Phase
- **`/pb-plan`** — Define pipeline stages, data schema, error scenarios
- **`/pb-adr`** — Decisions: why async/await, SQLAlchemy async, PostgreSQL

### Development
- **`/pb-start`** — Create feature branch, establish development rhythm
- **`/pb-cycle`** — Each pipeline stage: develop → test → commit
- **`/pb-guide-python`** — Language-specific patterns: async/await, pytest, SQLAlchemy

### Testing
- **`/pb-testing`** — Unit tests (async fixtures), integration tests (test database)
- Run: `make test` (uses pytest + pytest-asyncio)

### Code Quality
- **`/pb-standards`** — Code formatting, error handling patterns
- Run: `make fmt && make lint` (black, isort, flake8)

### Type Safety
- **`/pb-guide-python`** — Type hints and mypy checking
- Run: `make typecheck`

### Security
- **`/pb-patterns-security`** — SQL injection prevention (parameterized queries)
- **`/pb-security`** — Input validation in ingest stage

### Code Review
- **`/pb-cycle`** — Peer review each commit
- **`/pb-review-code`** — Multi-perspective review (testing, performance, async safety)

### Release & Deployment
- **`/pb-release`** — Pre-release checks
- **`/pb-deployment`** — Container deployment
- **`/pb-patterns-async`** — Async patterns for production

---

## Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (recommended)
- PostgreSQL 15 (if running without Docker)

### 1. Run with Docker Compose

```bash
cd examples/python-data-pipeline

# Generate sample data
python -c "
import csv
with open('sample_events.csv', 'w') as f:
    w = csv.DictWriter(f, ['user_id', 'event_type', 'data'])
    w.writeheader()
    w.writerows([
        {'user_id': '1', 'event_type': 'login', 'data': ''},
        {'user_id': '1', 'event_type': 'view_page', 'data': '/home'},
        {'user_id': '2', 'event_type': 'purchase', 'data': 'item_123'},
    ])
"

# Start pipeline and PostgreSQL
docker-compose up

# View logs
docker-compose logs pipeline
```

### 2. Develop Locally (Without Docker)

**Prerequisites:**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Create sample data
python -c "
import csv
with open('sample_events.csv', 'w') as f:
    w = csv.DictWriter(f, ['user_id', 'event_type', 'data'])
    w.writeheader()
    w.writerows([
        {'user_id': '1', 'event_type': 'login', 'data': ''},
        {'user_id': '2', 'event_type': 'view', 'data': '/home'},
    ])
"
```

**Run tests:**
```bash
make test         # Run all tests
make test-cov     # With coverage report
make typecheck    # Type checking
```

**Run pipeline:**
```bash
# Use SQLite (default, no setup needed)
make run

# Or use PostgreSQL
export DATABASE_URL="postgresql+asyncpg://user:password@localhost/db"
make run
```

### 3. Use Playbook Commands

#### Start a new feature
```bash
# From /pb-start
git checkout -b feature/v1.0.0-event-filtering main

# Make changes
# Run /pb-cycle for each iteration
```

#### Run quality checks
```bash
make fmt          # Format code
make lint         # Lint code
make typecheck    # Type checking
make test-cov     # Tests with coverage
```

#### Review code
```bash
# Use /pb-cycle at each iteration
# Use /pb-review-code for final review
```

#### Create PR
```bash
git push origin feature/v1.0.0-event-filtering
# Use /pb-pr to create PR with proper context
```

---

## Project Structure

```
python-data-pipeline/
├── src/
│   └── main.py              # Pipeline application (async orchestration)
├── tests/
│   └── test_pipeline.py     # Tests (pytest + pytest-asyncio)
├── docs/
│   ├── DEVELOPMENT.md       # Development workflow
│   ├── ARCHITECTURE.md      # System design, data flow
│   ├── TESTING.md           # Testing strategy
│   └── SECURITY.md          # Security checklist
├── docker-compose.yml       # Local development stack
├── Dockerfile               # Container image
├── Makefile                 # Build targets
├── requirements.txt         # Python dependencies
├── sample_events.csv        # Example data
└── README.md                # This file
```

---

## Key Patterns from Playbook

### 1. Async/Await (`/pb-guide-python`)
```python
# Concurrent I/O operations
async for event in pipeline.read_events_from_csv(filepath):
    # Process events asynchronously
```

### 2. SQLAlchemy Async ORM (`/pb-patterns-db`)
```python
# Connection pooling configured automatically
engine = create_async_engine(database_url, poolclass=NullPool)

# Transactions with rollback
async with session.begin():
    session.add(event)
    # Auto-rollback on exception
```

### 3. Error Handling (`/pb-guide-python` + `/pb-patterns-core`)
```python
try:
    # Operations
    await session.commit()
except Exception as e:
    await session.rollback()
    logger.error(f"Failed: {e}")
    raise
```

### 4. Testing (`/pb-testing` + `/pb-guide-python`)
```python
@pytest.mark.asyncio
async def test_ingest_events(pipeline):
    """Test with async fixture."""
    count = await pipeline.ingest_events(events)
    assert count == expected
```

### 5. Type Hints (`/pb-guide-python`)
```python
async def ingest_events(self, events: List[dict]) -> int:
    """Type hints for clarity and IDE support."""
```

### 6. Security (`/pb-security` + `/pb-patterns-security`)
```python
# Parameterized queries (no SQL injection)
await session.execute(
    sa.select(User).where(User.id == user_id)
)

# Input validation
if not event.get('user_id'):
    logger.warning("Skipping invalid event")
```

---

## How to Adapt This Project

### Fork It
```bash
cp -r examples/python-data-pipeline /path/to/my-pipeline
cd /path/to/my-pipeline
# Update pyproject.toml or requirements.txt with your package name
```

### Customize Pipeline Stages
1. Edit `read_events_from_csv()` to read your data source
2. Update `Event` and `EventSummary` models for your domain
3. Modify `ingest_events()` with your validation logic
4. Update `process_events()` with your aggregation logic

### Add New Stages
```python
async def export_summaries(self, output_file: str) -> None:
    """Export summaries to file."""
    summaries = await self.get_all_summaries()
    # Write to file, API, etc.
```

### Use Playbook Commands
- `/pb-plan` — Plan your pipeline
- `/pb-start` → `/pb-cycle` — Development iteration
- `/pb-testing` — Test strategy
- `/pb-release` — Release checklist

---

## Development Workflow

### Create a Feature

```bash
# Step 1: Plan (using /pb-plan)
# Define: data schema, pipeline stages, error handling

# Step 2: Start development (using /pb-start)
git checkout -b feature/v1.0.0-new-stage main

# Step 3: Each iteration (using /pb-cycle)
# - Write code
# - Self-review
# - Test (make test)
# - Commit (git commit with clear message)

# Step 4: Final review (using /pb-review-code)
# - Security perspective (pb-security checklist)
# - Testing perspective (pb-testing coverage)
# - Performance perspective (pb-performance profiling)

# Step 5: Release (using /pb-release)
# - Pre-release checks
# - Deploy to staging
# - Tag version: git tag v1.0.0
```

### Run Tests
```bash
make test           # Run all tests
make test-cov       # With coverage report
make test-asyncio   # Async-specific tests
```

### Code Quality
```bash
make fmt            # Format code (black + isort)
make lint           # Lint (flake8)
make typecheck      # Type checking (mypy)
```

---

## Integration with CI/CD

GitHub Actions workflow:
1. Checkout code
2. Setup Python 3.11
3. Install dependencies
4. Run linting (black, isort, flake8)
5. Run type checking (mypy)
6. Run tests with coverage
7. Build Docker image
8. (Optional) Push to registry

Uses playbook patterns:
- `/pb-guide-python` — Testing & async patterns
- `/pb-deployment` — Container deployment
- `/pb-release` — Release gates

---

## Database Schema

```sql
-- Events table
CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    event_data VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Event summaries (aggregated)
CREATE TABLE event_summaries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL,
    total_events INTEGER DEFAULT 0,
    last_event_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Async Best Practices (from `/pb-guide-python`)

✅ **Do:**
- Use `async for` for I/O operations
- Use `asyncio.gather()` for concurrent operations
- Always use `await` for async functions
- Use context managers for resource cleanup

❌ **Don't:**
- Block with `time.sleep()` (use `asyncio.sleep()`)
- Mix sync and async code without care
- Forget to `await` async functions
- Create goroutines without tracking them

---

## Performance Tips

- Use connection pooling (automatic with SQLAlchemy)
- Batch process events in chunks
- Use indexes on frequently-queried columns
- Profile with Python's cProfile tool

```bash
python -m cProfile -s cumulative -m src.main
```

---

## Related Playbook Commands

- `/pb-guide-python` — Python-specific SDLC guide (async, testing, deployment)
- `/pb-patterns-async` — Async patterns (callbacks, promises, async/await)
- `/pb-patterns-db` — Database patterns (pooling, transactions)
- `/pb-security` — Security checklist and patterns
- `/pb-testing` — Testing strategy and best practices
- `/pb-deployment` — Deployment and DevOps practices

---

## Support

For questions about:
- **Playbook patterns** → See `/pb-guide` or specific `/pb-*` command
- **Python development** → See `/pb-guide-python`
- **Async patterns** → See `/pb-patterns-async`
- **Database patterns** → See `/pb-patterns-db`
- **This example project** → See `docs/DEVELOPMENT.md`

---

*This example is part of the Engineering Playbook project.*
*Last updated: 2026-01-12*
