# Development Guide

How to develop on this Python data pipeline using the Playbook patterns.

---

## Setup

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (for local development with PostgreSQL)
- PostgreSQL 15 (if running without Docker)

### Initial Setup

```bash
# 1. Navigate to project
cd examples/python-data-pipeline

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start PostgreSQL with Docker Compose
docker-compose up postgres

# 5. In another terminal, run tests to verify setup
make test
```

Alternatively, start everything:
```bash
docker-compose up
# Pipeline runs and processes sample data
```

---

## Development Workflow

Follow the `/pb-start` and `/pb-cycle` pattern:

### 1. Start Work

```bash
# Create feature branch (following /pb-start pattern)
git checkout -b feature/v1.0.0-add-event-filtering main

# Verify setup
make test
```

### 2. Develop

Make changes to:
- `src/main.py` — Add pipeline stages, modify business logic
- `tests/test_pipeline.py` — Add tests

Example: Add a new pipeline stage

```python
# In src/main.py, add new method to Pipeline class:

async def filter_events(self, min_user_id: int = 0) -> int:
    """Filter events by user_id threshold."""
    async with self.async_session_factory() as session:
        try:
            # Delete events for users below threshold
            await session.execute(
                sa.delete(Event).where(Event.user_id < min_user_id)
            )
            await session.commit()
            return 1
        except Exception as e:
            await session.rollback()
            logger.error(f"Filter failed: {e}")
            raise
```

Then add to pipeline orchestration in `run_pipeline()`.

### 3. Self-Review (Using `/pb-cycle`)

Before committing, check:

```bash
# Format code (black + isort)
make fmt

# Check for lint issues
make lint

# Run type checking
make typecheck

# Run tests
make test

# Check coverage
make test-cov
```

### 4. Commit

```bash
# Logical, atomic commit
git add src/main.py tests/test_pipeline.py

git commit -m "feat(pipeline): add event filtering stage

- Filter events by user_id threshold
- Add tests for filtering logic
- Update pipeline orchestration"
```

Use this format:
```
<type>(<scope>): <subject>

<body>

- Specific changes made
- Why the change was needed
- Related issue/feature
```

### 5. Peer Review (Using `/pb-cycle`)

Push to GitHub and create PR:
```bash
git push origin feature/v1.0.0-add-event-filtering
# Then use /pb-pr command to create PR
```

Review checklist (from `/pb-guide-python`):
- [ ] `black` formatting applied
- [ ] `isort` imports sorted
- [ ] `flake8` passes (no linting errors)
- [ ] `mypy` passes (type checking)
- [ ] `pytest` passes with >70% coverage
- [ ] No `import *` (explicit imports)
- [ ] All async functions tested with `@pytest.mark.asyncio`
- [ ] Type hints on all public functions
- [ ] Docstrings on complex functions
- [ ] No hardcoded secrets or credentials
- [ ] Error handling explicit (no silent failures)
- [ ] SQL queries are parameterized (no injection risks)

---

## Testing

### Run Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test class
pytest -v tests/test_pipeline.py::TestEventIngestion

# Run specific test function
pytest -v tests/test_pipeline.py::TestEventIngestion::test_ingest_events_success

# Run async tests with verbose output
make test-asyncio
```

### Write Tests

Use async fixtures (pytest-asyncio):

```python
@pytest.mark.asyncio
async def test_process_events(pipeline):
    """Test event processing stage."""
    # Arrange
    events = [
        {'user_id': '1', 'event_type': 'login', 'data': ''},
        {'user_id': '2', 'event_type': 'view', 'data': '/home'},
    ]
    await pipeline.ingest_events(events)

    # Act
    user_count = await pipeline.process_events()

    # Assert
    assert user_count == 2
    summaries = await pipeline.get_all_summaries()
    assert len(summaries) == 2
```

### Test Database

Tests use SQLite in-memory by default. For PostgreSQL tests:
```bash
# Start PostgreSQL container
docker-compose up postgres

# Run tests with PostgreSQL
DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost/test_db" make test
```

---

## Common Tasks

### Add a New Pipeline Stage

1. **Add method to Pipeline class in `src/main.py`:**

```python
async def enrich_events(self) -> int:
    """Enrich events with additional data."""
    async with self.async_session_factory() as session:
        try:
            result = await session.execute(
                sa.select(Event).where(Event.event_data == '')
            )
            events = result.scalars().all()

            for event in events:
                # Enrich event_data
                event.event_data = f"enriched_{event.event_type}"

            await session.commit()
            logger.info(f"Enriched {len(events)} events")
            return len(events)

        except Exception as e:
            await session.rollback()
            logger.error(f"Enrichment failed: {e}")
            raise
```

2. **Update pipeline orchestration in `run_pipeline()`:**

```python
async def run_pipeline(database_url: str, csv_filepath: str) -> None:
    pipeline = Pipeline(database_url)

    try:
        await pipeline.initialize()

        # Read and ingest
        events = []
        async for event in pipeline.read_events_from_csv(csv_filepath):
            events.append(event)
        await pipeline.ingest_events(events)

        # Process
        await pipeline.process_events()

        # NEW: Enrich
        await pipeline.enrich_events()

        # Report
        summaries = await pipeline.get_all_summaries()
        logger.info(f"Generated {len(summaries)} summaries")

    finally:
        await pipeline.close()
```

3. **Add tests in `tests/test_pipeline.py`:**

```python
@pytest.mark.asyncio
async def test_enrich_events(pipeline):
    """Test event enrichment stage."""
    # Setup
    events = [
        {'user_id': '1', 'event_type': 'login', 'data': ''},
    ]
    await pipeline.ingest_events(events)

    # Test
    count = await pipeline.enrich_events()

    assert count == 1
```

4. **Test and commit:**

```bash
make test
git add src/main.py tests/test_pipeline.py
git commit -m "feat(pipeline): add event enrichment stage"
```

### Modify Database Schema

Edit models in `src/main.py`:

```python
class Event(Base):
    __tablename__ = 'events'

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, nullable=False, index=True)
    event_type = sa.Column(sa.String(50), nullable=False)
    event_data = sa.Column(sa.String(500))
    severity = sa.Column(sa.String(20), default='info')  # NEW
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)
```

### Add Logging

Use structured logging (from `/pb-guide-python`):

```python
logger.info("Event processed", extra={
    'user_id': event.user_id,
    'event_type': event.event_type,
    'duration_ms': elapsed_ms
})

logger.error("Pipeline failed", extra={
    'stage': 'enrichment',
    'error': str(e)
})
```

---

## Debugging

### View Logs

```bash
# If running with docker-compose
docker-compose logs -f pipeline

# If running locally, logs appear in stdout
# Increase verbosity:
export LOGLEVEL=DEBUG
make run
```

### Database Inspection

```bash
# Connect to PostgreSQL
psql -U postgres -d playbook_db

# Show events
SELECT * FROM events LIMIT 10;

# Count by user
SELECT user_id, COUNT(*) FROM events GROUP BY user_id;

# Show summaries
SELECT * FROM event_summaries;
```

### API Testing / Interactive

```python
# Create interactive Python shell
python

# Import and test
from src.main import Pipeline
import asyncio

pipeline = Pipeline('sqlite+aiosqlite:///test.db')
asyncio.run(pipeline.initialize())

# Run async code
events = [{'user_id': '1', 'event_type': 'test', 'data': ''}]
asyncio.run(pipeline.ingest_events(events))
```

---

## Code Quality Gates

Before every commit, check:

```bash
# 1. Format
make fmt

# 2. Lint
make lint

# 3. Type check
make typecheck

# 4. Test
make test

# 5. Coverage check
make test-cov
```

Never skip these gates. They catch bugs early.

---

## Performance Testing

### Profile Execution

```bash
# Profile the pipeline
python -m cProfile -s cumulative -m src.main

# More detailed profiling
python -m py_spy record -o profile.svg -- python -m src.main
```

### Memory Usage

```bash
# Monitor memory while running
python -m memory_profiler src/main.py

# Or use psutil
pip install psutil
```

### Async Performance

```python
import asyncio
import time

async def benchmark():
    start = time.time()
    # Your async code
    await pipeline.process_events()
    elapsed = time.time() - start
    print(f"Processed in {elapsed:.2f}s")

asyncio.run(benchmark())
```

---

## Type Hints & MyPy

Ensure full type coverage:

```bash
# Check for missing type hints
mypy src/ --disallow-untyped-defs

# Check with strict mode
mypy src/ --strict
```

Add type hints to all functions:

```python
# Good
async def ingest_events(self, events: List[dict]) -> int:
    """Ingest events into database."""

# Bad
async def ingest_events(self, events):
    # Missing type hints!
```

---

## Troubleshooting

### "Module not found" errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python path
python -c "import sys; print(sys.path)"
```

### "Connection refused" on database

```bash
# Check if PostgreSQL is running
docker-compose ps

# Start if needed
docker-compose up postgres -d

# Check logs
docker-compose logs postgres
```

### Async test failures

```bash
# Make sure pytest-asyncio is installed
pip install pytest-asyncio

# Run with asyncio plugin
pytest -p pytest_asyncio tests/
```

### Type checking fails

```bash
# Update mypy
pip install --upgrade mypy

# Ignore third-party libraries if needed
mypy src/ --ignore-missing-imports
```

---

## Integration with Playbook

This development workflow follows:
- `/pb-start` — Branch creation, initial setup
- `/pb-cycle` — Develop → Self-review → Test → Commit
- `/pb-guide-python` — Python-specific patterns and tools
- `/pb-testing` — Testing strategy
- `/pb-review-cleanup` — Code review checklist

---

*For more details, see parent `README.md` or Playbook commands.*
