# Python SDLC Playbook

Language-specific guide for Python projects. Use alongside `/pb-guide` for general process.

**Principle:** Language-specific guidance still assumes `/pb-preamble` thinking. Challenge Python conventions if they don't fit. Adapt this guide to your project—it's a starting point.

---

## **Python-Specific Change Tiers**

Adapt tier based on Python complexity:

| Tier | Examples | Key Considerations |
|------|----------|-------------------|
| **XS** | Typo, config constant, import cleanup | Lint check: `black`, `isort`, `flake8` |
| **S** | Bug in single handler, type annotation | Test one module: `pytest tests/test_handler.py` |
| **M** | New endpoint, ORM model change | Test full suite: `pytest --cov` |
| **L** | New async service, architectural change | Type check: `mypy`, async testing |

---

## **Python Project Structure**

Standard Python project layout:

```
myproject/
├── src/myproject/
│   ├── __init__.py
│   ├── main.py                  # Entry point (Flask/FastAPI app)
│   ├── api/                     # HTTP endpoints
│   │   └── handlers.py
│   ├── services/                # Business logic
│   │   └── user_service.py
│   ├── repositories/            # Data access layer
│   │   └── user_repository.py
│   ├── models/                  # Data structures, ORM models
│   │   └── user.py
│   ├── middleware/              # Request/response middleware
│   └── config.py                # Configuration
├── tests/
│   ├── test_handlers.py
│   ├── test_services.py
│   └── conftest.py              # Shared fixtures
├── requirements.txt             # Dependencies (or pyproject.toml)
├── Dockerfile
├── Makefile                     # Build targets
├── pytest.ini                   # Test configuration
└── README.md
```

---

## **1. Intake & Clarification (Python-Specific)**

### **1.1 Python-Specific Requirements**

Document async and performance expectations:
- **Async model:** sync (threading), async/await (asyncio), or celery tasks?
- **Performance budget:** response time targets, concurrency limits
- **Python version:** 3.8, 3.9, 3.10, or 3.11+?
- **Async framework:** FastAPI, Flask + asyncio, or custom?
- **Type hints:** Required? Tools like `mypy` configured?

### **1.2 Virtual Environment Setup**

Before starting:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Verify dependencies
pip list
pip check  # Check for dependency conflicts
```

### **1.3 Type Checking**

Establish type checking baseline:
```bash
mypy src/  # Check for type errors
```

---

## **2. Stakeholder Alignment**

### **2.1 Infrastructure & Ops**

Ensure agreement on:
- **Deployment:** WSGI (Gunicorn), ASGI (Uvicorn), or serverless?
- **Database ORM:** SQLAlchemy, Django ORM, or raw SQL?
- **Async support:** Do we need async/await or is threading OK?
- **Dependency isolation:** Docker or virtualenv?
- **Python version:** Does production need 3.10+ for newer syntax?

### **2.2 Performance Expectations**

Discuss with stakeholders:
```
Response time: <200ms for typical requests
Throughput: X requests/second (if known)
Memory: <500MB baseline + per-request overhead
Concurrency: threading, async, or process-based?
```

---

## **3. Python-Specific Requirements Definition**

### **3.1 Async Model**

Define how concurrency will work:

**In-Scope Example:**
- Requests handled via FastAPI (async endpoints)
- Service layer uses async/await for I/O
- Background tasks with Celery for long-running jobs
- Type hints for all public functions

**Out-of-Scope Example:**
- Don't add new database migrations (use existing pattern)
- Don't change logging configuration
- Don't modify docker entrypoint

### **3.2 Dependencies**

List required packages:

```
# Web framework
fastapi            # Modern async web framework
uvicorn            # ASGI server
starlette          # Underlying async framework

# Database
sqlalchemy         # ORM
alembic            # Migrations
psycopg2-binary    # PostgreSQL driver

# Async job processing
celery             # Task queue
redis              # Message broker

# Testing
pytest             # Testing framework
pytest-asyncio     # Async test support
pytest-cov         # Coverage reporting

# Code quality
black              # Code formatter
isort              # Import sorter
flake8             # Linter
mypy               # Type checker

# Logging
structlog          # Structured logging
```

Add to `requirements.txt` or `pyproject.toml`:
```
fastapi==0.104.0
sqlalchemy==2.0.23
celery==5.3.4
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.11.0
mypy==1.7.0
```

### **3.3 Type Hints**

Define type hint requirements:
```python
# All public functions require type hints
def get_user(user_id: int) -> Optional[User]:
    pass

# All class attributes require type hints (or use @dataclass)
class UserService:
    db: Database
    cache: Redis

# Use Optional, List, Dict for complex types
def get_users(ids: List[int]) -> Dict[int, User]:
    pass
```

### **3.4 Async Patterns**

Define async usage:

```
Pattern 1: FastAPI async endpoints (default for web)
  GET /api/users/{id} → async def get_user() → Service → Response

Pattern 2: Background jobs
  POST /api/email → Queue task → Celery worker → Send email → Log result

Pattern 3: Streaming/SSE
  GET /api/stream → async generator → Client receives events
```

---

## **4. Python Architecture & Design**

### **4.1 Standard Python Architecture (FastAPI)**

```
HTTP Request
    ↓
FastAPI Middleware (auth, logging, timing)
    ↓
Endpoint Handler (api/handlers.py)
    ↓
Service Layer (services/user_service.py)
    ↓
Repository Layer (repositories/user_repository.py)
    ↓
Database / Cache
```

### **4.2 Async Pattern**

**For typical web service:**

```python
# [YES] Async/await for I/O operations
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> User:
    """Async endpoint - doesn't block on I/O."""
    user = await db.get(User, user_id)
    return user

@app.post("/users")
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)) -> User:
    """Create user with async database access."""
    user = User(**data.dict())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


# [YES] Concurrent I/O with asyncio.gather
import asyncio

async def get_user_with_posts(user_id: int, db: AsyncSession) -> dict:
    """Fetch user and posts concurrently."""
    user_coro = db.get(User, user_id)
    posts_coro = db.execute(
        select(Post).where(Post.user_id == user_id)
    )

    user, posts_result = await asyncio.gather(user_coro, posts_coro)
    return {"user": user, "posts": posts_result.scalars().all()}


# [NO] Blocking I/O (blocks event loop)
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)) -> User:
    # This blocks the entire server - don't use for sync I/O!
    user = db.query(User).get(user_id)  # BLOCKS
    return user
```

**For background jobs:**

```python
# Use Celery for long-running tasks
from celery import shared_task
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_welcome_email(self, user_id: int):
    """Send welcome email asynchronously."""
    try:
        user = get_user(user_id)
        email_service.send(
            to=user.email,
            subject="Welcome!",
            template="welcome"
        )
        logger.info(f"Email sent to user {user_id}")

    except Exception as exc:
        logger.error(f"Failed to send email: {exc}")
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)

# Queue task from endpoint (returns immediately)
@app.post("/users")
async def create_user(data: UserCreate, db: AsyncSession) -> User:
    user = User(**data.dict())
    await db.commit()

    # Send email asynchronously
    send_welcome_email.delay(user.id)

    return user
```

### **4.3 Error Handling Pattern**

```python
# [YES] Explicit error handling
from fastapi import HTTPException, status

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession) -> User:
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found"
        )
    return user


# [YES] Custom exceptions
class UserNotFoundError(Exception):
    """Raised when user doesn't exist."""
    pass

@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )


# [NO] Swallowing exceptions
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession) -> User:
    try:
        user = await db.get(User, user_id)
    except Exception:
        pass  # NEVER swallow exceptions!
    return user  # Returns None silently
```

### **4.4 Dependency Injection (FastAPI)**

```python
from fastapi import Depends

# Define dependencies
async def get_db() -> AsyncSession:
    """Get database session."""
    async with get_async_session() as session:
        yield session

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Verify token and return user."""
    payload = jwt.decode(token, SECRET_KEY)
    user_id = payload.get("sub")
    return await get_user(user_id)

# Inject dependencies into handlers
@app.get("/me")
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> User:
    return current_user
```

---

## **5. Implementation (Python-Specific)**

### **5.1 Code Quality Tools**

Required for all commits:

```bash
# Format code (enforced)
black src/
isort src/

# Lint code
flake8 src/ --max-line-length=120
pylint src/

# Type checking
mypy src/ --ignore-missing-imports

# Dependency audit
pip check

# All together (add to pre-commit hook)
black src/ && isort src/ && flake8 src/ && mypy src/
```

### **5.2 Testing Patterns**

**Unit Test Structure (pytest):**

```python
import pytest
from unittest.mock import patch, AsyncMock

class TestUserService:
    """Test UserService class."""

    @pytest.fixture
    def mock_repo(self):
        """Mock repository fixture."""
        mock = AsyncMock()
        return mock

    @pytest.mark.asyncio
    async def test_get_user_success(self, mock_repo):
        """Test getting existing user."""
        # Arrange
        mock_repo.get_user.return_value = User(
            id=1, name="John", email="john@example.com"
        )
        service = UserService(repo=mock_repo)

        # Act
        user = await service.get_user(user_id=1)

        # Assert
        assert user.id == 1
        assert user.name == "John"
        mock_repo.get_user.assert_called_once_with(1)

    @pytest.mark.asyncio
    async def test_get_user_not_found(self, mock_repo):
        """Test getting non-existent user."""
        mock_repo.get_user.return_value = None
        service = UserService(repo=mock_repo)

        with pytest.raises(UserNotFoundError):
            await service.get_user(user_id=999)
```

**Integration Test:**

```python
@pytest.mark.asyncio
async def test_create_user_integration(async_db: AsyncSession):
    """Test full user creation flow."""
    # Create user via service
    service = UserService(repo=UserRepository(async_db))
    user = await service.create_user(
        name="Alice",
        email="alice@example.com"
    )

    # Verify in database
    db_user = await async_db.get(User, user.id)
    assert db_user.name == "Alice"
    assert db_user.email == "alice@example.com"
```

**Async Test Fixture:**

```python
@pytest.fixture
async def async_db():
    """Create test database session."""
    async_engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:"
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )

    yield async_session()

    await async_engine.dispose()
```

### **5.3 Async Best Practices**

```python
# [YES] Use async/await for concurrent I/O
import asyncio

async def fetch_users_concurrently(user_ids: List[int]) -> List[User]:
    """Fetch multiple users concurrently."""
    # Create coroutines for each fetch
    coros = [fetch_user(uid) for uid in user_ids]

    # Execute all concurrently
    users = await asyncio.gather(*coros)
    return users

# [YES] Use asyncio.TimeoutError for timeouts
async def get_user_with_timeout(user_id: int, timeout: int = 5) -> User:
    """Get user with timeout."""
    try:
        user = await asyncio.wait_for(
            fetch_user(user_id),
            timeout=timeout
        )
        return user
    except asyncio.TimeoutError:
        logger.error(f"User fetch timed out after {timeout}s")
        raise

# [YES] Use context managers for resource cleanup
async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        data = await response.json()

# [NO] Blocking calls in async code
async def get_users(db: AsyncSession) -> List[User]:
    # Don't mix sync database calls with async code
    users = db.query(User).all()  # BLOCKS! Use await instead
    return users
```

### **5.4 Database Patterns (SQLAlchemy)**

**Async ORM:**
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Create async engine
engine = create_async_engine("postgresql+asyncpg://user:password@localhost/db")

# Create async session factory
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Query pattern
async with async_session() as session:
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    return user
```

**Transaction Pattern:**
```python
async def update_user(user_id: int, data: UserUpdate) -> User:
    """Update user in transaction."""
    async with async_session() as session:
        # Start transaction
        async with session.begin():
            user = await session.get(User, user_id)
            if not user:
                raise UserNotFoundError(f"User {user_id} not found")

            # Update user
            for key, value in data.dict().items():
                setattr(user, key, value)

            await session.flush()  # Insert/update
            # On success, transaction commits automatically
            return user
```

---

## **6. Testing Readiness (Python-Specific)**

### **6.1 Test Coverage Requirements**

| Tier | Coverage | Command |
|------|----------|---------|
| **S** | >50% | `pytest --cov=src tests/` |
| **M** | >70% | `pytest --cov=src --cov-fail-under=70 tests/` |
| **L** | >80% | `pytest --cov=src --cov-fail-under=80 tests/` |

```bash
# Generate coverage report
pytest --cov=src --cov-report=html tests/
open htmlcov/index.html

# Run with timeout (prevent hanging tests)
pytest --timeout=5 tests/
```

### **6.2 Test Organization**

```
tests/
├── test_handlers.py      # API endpoint tests
├── test_services.py      # Business logic tests
├── test_repositories.py  # Data access tests
├── conftest.py           # Shared fixtures
└── fixtures/
    └── sample_data.py    # Test data
```

**conftest.py Example:**
```python
import pytest
from sqlalchemy.ext.asyncio import create_async_engine

@pytest.fixture
async def test_db():
    """In-memory test database."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
def client():
    """FastAPI test client."""
    from fastapi.testclient import TestClient
    from app import app
    return TestClient(app)
```

---

## **7. Code Review Checklist (Python-Specific)**

Before PR review:

- [ ] `black` formatting applied
- [ ] `isort` imports sorted
- [ ] `flake8` passes (no linting errors)
- [ ] `mypy` passes (type checking)
- [ ] `pytest` passes with >70% coverage
- [ ] No `import *` (explicit imports)
- [ ] All async functions tested with `@pytest.mark.asyncio`
- [ ] Type hints on all public functions
- [ ] Docstrings on complex functions/classes
- [ ] No hardcoded secrets or credentials
- [ ] Error handling explicit (no silent failures)
- [ ] Dependencies in `requirements.txt` or `pyproject.toml`

---

## **8. Deployment (Python-Specific)**

### **8.1 Application Server**

**ASGI (Async, Recommended):**
```bash
# Install gunicorn and uvicorn workers
pip install gunicorn uvicorn

# Run with async workers
gunicorn \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  -b 0.0.0.0:8000 \
  app:app
```

**WSGI (Sync, if needed):**
```bash
# Install gunicorn
pip install gunicorn

# Run with sync workers
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### **8.2 Container Image**

```dockerfile
# Multi-stage build
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY . /app
WORKDIR /app

EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "app:app"]
```

### **8.3 Graceful Shutdown**

```python
import signal
import asyncio

async def main():
    app = create_app()
    server = uvicorn.Server(uvicorn.Config(app))

    # Handle shutdown signals
    def handle_signal(signum, frame):
        asyncio.create_task(server.shutdown())

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
```

---

## **9. Observability (Python-Specific)**

### **9.1 Structured Logging**

```python
import structlog

logger = structlog.get_logger()

# Log with context
logger.info(
    "user_created",
    user_id=user_id,
    email=user_email,
    duration_ms=elapsed
)

# Error with exception info
try:
    result = await get_data()
except Exception as e:
    logger.exception("failed_to_get_data", error=str(e))
```

### **9.2 Metrics (Prometheus)**

```python
from prometheus_client import Counter, Histogram

# Counter for requests
http_requests = Counter(
    'http_requests_total',
    'HTTP requests',
    ['method', 'endpoint', 'status']
)

# Histogram for latency
http_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

# In FastAPI middleware
@app.middleware("http")
async def add_metrics(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    http_requests.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    http_duration.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    return response
```

### **9.3 Profiling**

```python
# Profile CPU usage
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# ... code to profile ...

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 functions
```

---

## **10. Release & Post-Release**

### **10.1 Release Checklist**

- [ ] All tests pass: `pytest tests/`
- [ ] Coverage >70%: `pytest --cov=src tests/`
- [ ] Type checking passes: `mypy src/`
- [ ] Code quality OK: `black`, `isort`, `flake8`
- [ ] Dependencies up-to-date: `pip list`
- [ ] Docker image built and pushed
- [ ] Migrations applied (if DB changes)
- [ ] Rollback plan documented
- [ ] Monitoring alerts configured

### **10.2 Rollback**

If deployed version has issues:

```bash
# Revert to previous version
git checkout v1.2.2
pip install -r requirements.txt
python -m alembic downgrade -1  # Revert migrations
# Deploy previous container/code
```

### **10.3 Post-Release Monitoring**

Monitor for:
- Error rates (logs, alerts)
- Response time (p50, p95, p99)
- Memory usage (shouldn't grow unbounded)
- Worker status (Celery, Uvicorn)

```python
# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "version": VERSION,
        "timestamp": datetime.now().isoformat()
    }
```

---

## **Integration with Playbook**

**Related Commands:**
- `/pb-guide` — General SDLC process
- `/pb-patterns-core` — Architectural patterns
- `/pb-patterns-async` — Async/concurrency patterns
- `/pb-performance` — Performance optimization
- `/pb-testing` — Advanced testing strategies
- `/pb-deployment` — Deployment and DevOps

---

*Created: 2026-01-11 | Category: Language Guides | Language: Python | Tier: L*
