"""
Tests for the data pipeline.

Demonstrates pytest patterns from /pb-guide-python:
- Async fixtures with pytest-asyncio
- Mocking and patching
- Table-driven tests
- Integration tests with test database
"""

import asyncio
import csv
import tempfile
from datetime import datetime
from pathlib import Path
from typing import List

import pytest
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Import pipeline classes
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from main import Base, Event, EventSummary, Pipeline


@pytest.fixture
async def test_database():
    """Create in-memory test database."""
    database_url = 'sqlite+aiosqlite:///:memory:'
    engine = create_async_engine(database_url, echo=False)

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Cleanup
    await engine.dispose()


@pytest.fixture
async def pipeline(test_database):
    """Create pipeline with test database."""
    database_url = 'sqlite+aiosqlite:///:memory:'
    pipeline = Pipeline(database_url)
    await pipeline.initialize()

    yield pipeline

    await pipeline.close()


@pytest.fixture
def sample_events_csv():
    """Create sample CSV file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.DictWriter(f, fieldnames=['user_id', 'event_type', 'data'])
        writer.writeheader()
        writer.writerows([
            {'user_id': '1', 'event_type': 'login', 'data': ''},
            {'user_id': '1', 'event_type': 'view_page', 'data': '/home'},
            {'user_id': '2', 'event_type': 'login', 'data': ''},
            {'user_id': '2', 'event_type': 'purchase', 'data': 'product_123'},
            {'user_id': '3', 'event_type': 'logout', 'data': ''},
        ])
        filepath = f.name

    yield filepath

    # Cleanup
    Path(filepath).unlink()


class TestPipelineInitialization:
    """Test pipeline initialization."""

    @pytest.mark.asyncio
    async def test_initialize_creates_tables(self, pipeline):
        """Test that initialize creates database tables."""
        assert pipeline.engine is not None
        assert pipeline.async_session_factory is not None

    @pytest.mark.asyncio
    async def test_close_disposes_engine(self, pipeline):
        """Test that close disposes the engine."""
        engine = pipeline.engine
        await pipeline.close()
        assert pipeline.engine is None


class TestEventIngestion:
    """Test event ingestion."""

    @pytest.mark.asyncio
    async def test_ingest_events_success(self, pipeline):
        """Test ingesting valid events."""
        events = [
            {'user_id': '1', 'event_type': 'login', 'data': ''},
            {'user_id': '2', 'event_type': 'view', 'data': '/home'},
        ]

        count = await pipeline.ingest_events(events)

        assert count == 2

    @pytest.mark.asyncio
    async def test_ingest_events_empty_list(self, pipeline):
        """Test ingesting empty event list."""
        count = await pipeline.ingest_events([])

        assert count == 0

    @pytest.mark.asyncio
    async def test_ingest_events_skips_invalid(self, pipeline):
        """Test that invalid events are skipped."""
        events = [
            {'user_id': '1', 'event_type': 'login', 'data': ''},
            {'user_id': '', 'event_type': 'view'},  # Invalid: no user_id
            {'user_id': '2', 'event_type': 'purchase', 'data': 'item_123'},
        ]

        count = await pipeline.ingest_events(events)

        # Should skip the invalid event
        assert count == 2


class TestEventProcessing:
    """Test event processing and summary generation."""

    @pytest.mark.asyncio
    async def test_process_events_generates_summaries(self, pipeline):
        """Test that processing generates summaries."""
        # Ingest test events
        events = [
            {'user_id': '1', 'event_type': 'login', 'data': ''},
            {'user_id': '1', 'event_type': 'view', 'data': '/home'},
            {'user_id': '2', 'event_type': 'login', 'data': ''},
        ]
        await pipeline.ingest_events(events)

        # Process events
        user_count = await pipeline.process_events()

        assert user_count == 2

    @pytest.mark.asyncio
    async def test_process_events_no_events(self, pipeline):
        """Test processing when no events exist."""
        user_count = await pipeline.process_events()

        assert user_count == 0


class TestEventRetrieval:
    """Test retrieving event summaries."""

    @pytest.mark.asyncio
    async def test_get_summary_success(self, pipeline):
        """Test getting summary for existing user."""
        # Setup
        events = [
            {'user_id': '1', 'event_type': 'login', 'data': ''},
            {'user_id': '1', 'event_type': 'view', 'data': '/home'},
        ]
        await pipeline.ingest_events(events)
        await pipeline.process_events()

        # Test
        summary = await pipeline.get_summary(1)

        assert summary is not None
        assert summary['user_id'] == 1
        assert summary['total_events'] == 2

    @pytest.mark.asyncio
    async def test_get_summary_not_found(self, pipeline):
        """Test getting summary for non-existent user."""
        summary = await pipeline.get_summary(999)

        assert summary is None

    @pytest.mark.asyncio
    async def test_get_all_summaries(self, pipeline):
        """Test getting all summaries."""
        # Setup
        events = [
            {'user_id': '1', 'event_type': 'login', 'data': ''},
            {'user_id': '2', 'event_type': 'login', 'data': ''},
            {'user_id': '3', 'event_type': 'login', 'data': ''},
        ]
        await pipeline.ingest_events(events)
        await pipeline.process_events()

        # Test
        summaries = await pipeline.get_all_summaries()

        assert len(summaries) == 3
        assert all('user_id' in s for s in summaries)


class TestCSVReading:
    """Test CSV file reading."""

    @pytest.mark.asyncio
    async def test_read_events_from_csv(self, pipeline, sample_events_csv):
        """Test reading events from CSV file."""
        events = []
        async for event in pipeline.read_events_from_csv(sample_events_csv):
            events.append(event)

        assert len(events) == 5
        assert events[0]['user_id'] == '1'
        assert events[0]['event_type'] == 'login'

    @pytest.mark.asyncio
    async def test_read_events_file_not_found(self, pipeline):
        """Test reading from non-existent file."""
        with pytest.raises(FileNotFoundError):
            async for _ in pipeline.read_events_from_csv('/nonexistent/file.csv'):
                pass


class TestEndToEndPipeline:
    """End-to-end pipeline tests."""

    @pytest.mark.asyncio
    async def test_complete_pipeline_flow(self, pipeline, sample_events_csv):
        """Test complete pipeline flow from CSV to summaries."""
        # Read and ingest
        events = []
        async for event in pipeline.read_events_from_csv(sample_events_csv):
            events.append(event)

        await pipeline.ingest_events(events)

        # Process
        await pipeline.process_events()

        # Verify summaries
        summaries = await pipeline.get_all_summaries()

        assert len(summaries) == 3
        assert summaries[0]['total_events'] == 2  # User 1 has 2 events
        assert summaries[1]['total_events'] == 2  # User 2 has 2 events
        assert summaries[2]['total_events'] == 1  # User 3 has 1 event


# Parametrized test example (table-driven style)
@pytest.mark.parametrize(
    'user_id,event_type,should_be_valid',
    [
        (1, 'login', True),
        (2, 'view', True),
        (3, 'purchase', True),
        ('', 'login', False),  # Invalid: empty user_id
        (None, 'view', False),  # Invalid: None user_id
    ],
    ids=['valid_login', 'valid_view', 'valid_purchase', 'empty_user_id', 'none_user_id'],
)
def test_event_validation(user_id, event_type, should_be_valid):
    """Test event validation with parametrized inputs."""
    event = {
        'user_id': str(user_id) if user_id is not None else '',
        'event_type': event_type,
    }

    is_valid = bool(event.get('user_id') and event.get('event_type'))
    assert is_valid == should_be_valid
