"""
Data pipeline for processing user events and generating reports.

This pipeline demonstrates:
- Async/await patterns (pb-guide-python)
- Database operations (SQLAlchemy)
- Error handling and logging
- Type hints
- Testing patterns
"""

import asyncio
import csv
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import AsyncGenerator, List, Optional

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# SQLAlchemy setup
Base = declarative_base()


class Event(Base):
    """User event model."""

    __tablename__ = 'events'

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, nullable=False, index=True)
    event_type = sa.Column(sa.String(50), nullable=False)
    event_data = sa.Column(sa.String(500))
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)


class EventSummary(Base):
    """Summary of events per user."""

    __tablename__ = 'event_summaries'

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, nullable=False, unique=True, index=True)
    total_events = sa.Column(sa.Integer, default=0)
    last_event_at = sa.Column(sa.DateTime)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)
    updated_at = sa.Column(sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Pipeline:
    """Data processing pipeline."""

    def __init__(self, database_url: str):
        """Initialize pipeline with database connection."""
        self.database_url = database_url
        self.engine = None
        self.async_session_factory = None

    async def initialize(self) -> None:
        """Initialize database connections and schema."""
        logger.info("Initializing pipeline...")

        # Create async engine
        self.engine = create_async_engine(
            self.database_url,
            echo=False,
            poolclass=NullPool,  # Recommended for async
        )

        # Create session factory
        self.async_session_factory = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

        # Create tables
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        logger.info("Pipeline initialized successfully")

    async def close(self) -> None:
        """Close database connections."""
        if self.engine:
            await self.engine.dispose()
            logger.info("Pipeline closed")

    async def read_events_from_csv(self, filepath: str) -> AsyncGenerator[dict, None]:
        """Read events from CSV file."""
        logger.info(f"Reading events from {filepath}")

        if not Path(filepath).exists():
            raise FileNotFoundError(f"CSV file not found: {filepath}")

        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                raise ValueError("CSV file is empty or invalid")

            for row in reader:
                yield row

    async def ingest_events(self, events: List[dict]) -> int:
        """Ingest events into database."""
        logger.info(f"Ingesting {len(events)} events")

        if not events:
            logger.warning("No events to ingest")
            return 0

        async with self.async_session_factory() as session:
            try:
                for event_data in events:
                    # Validate required fields
                    if not event_data.get('user_id') or not event_data.get('event_type'):
                        logger.warning(f"Skipping invalid event: {event_data}")
                        continue

                    event = Event(
                        user_id=int(event_data['user_id']),
                        event_type=event_data['event_type'],
                        event_data=event_data.get('data', ''),
                    )
                    session.add(event)

                await session.commit()
                logger.info(f"Successfully ingested {len(events)} events")
                return len(events)

            except Exception as e:
                await session.rollback()
                logger.error(f"Error ingesting events: {e}")
                raise

    async def process_events(self) -> int:
        """Process events and generate summaries."""
        logger.info("Processing events...")

        async with self.async_session_factory() as session:
            try:
                # Get all events
                result = await session.execute(
                    sa.select(Event).order_by(Event.user_id)
                )
                events = result.scalars().all()

                if not events:
                    logger.warning("No events to process")
                    return 0

                # Group by user_id
                user_events = {}
                for event in events:
                    if event.user_id not in user_events:
                        user_events[event.user_id] = []
                    user_events[event.user_id].append(event)

                # Generate summaries
                for user_id, user_event_list in user_events.items():
                    # Check if summary exists
                    result = await session.execute(
                        sa.select(EventSummary).where(
                            EventSummary.user_id == user_id
                        )
                    )
                    summary = result.scalar_one_or_none()

                    if summary:
                        # Update existing summary
                        summary.total_events = len(user_event_list)
                        summary.last_event_at = max(e.created_at for e in user_event_list)
                        summary.updated_at = datetime.utcnow()
                    else:
                        # Create new summary
                        summary = EventSummary(
                            user_id=user_id,
                            total_events=len(user_event_list),
                            last_event_at=max(e.created_at for e in user_event_list),
                        )
                        session.add(summary)

                await session.commit()
                logger.info(f"Successfully processed events for {len(user_events)} users")
                return len(user_events)

            except Exception as e:
                await session.rollback()
                logger.error(f"Error processing events: {e}")
                raise

    async def get_summary(self, user_id: int) -> Optional[dict]:
        """Get summary for a specific user."""
        async with self.async_session_factory() as session:
            result = await session.execute(
                sa.select(EventSummary).where(EventSummary.user_id == user_id)
            )
            summary = result.scalar_one_or_none()

            if summary:
                return {
                    'user_id': summary.user_id,
                    'total_events': summary.total_events,
                    'last_event_at': summary.last_event_at.isoformat() if summary.last_event_at else None,
                }
            return None

    async def get_all_summaries(self) -> List[dict]:
        """Get all event summaries."""
        async with self.async_session_factory() as session:
            result = await session.execute(
                sa.select(EventSummary).order_by(EventSummary.user_id)
            )
            summaries = result.scalars().all()

            return [
                {
                    'user_id': s.user_id,
                    'total_events': s.total_events,
                    'last_event_at': s.last_event_at.isoformat() if s.last_event_at else None,
                }
                for s in summaries
            ]


async def run_pipeline(database_url: str, csv_filepath: str) -> None:
    """Run the complete pipeline."""
    pipeline = Pipeline(database_url)

    try:
        await pipeline.initialize()

        # Read events from CSV
        events = []
        async for event in pipeline.read_events_from_csv(csv_filepath):
            events.append(event)

        # Ingest events
        if events:
            await pipeline.ingest_events(events)

        # Process events
        await pipeline.process_events()

        # Get and log summaries
        summaries = await pipeline.get_all_summaries()
        logger.info(f"Generated {len(summaries)} summaries")
        for summary in summaries:
            logger.info(f"User {summary['user_id']}: {summary['total_events']} events")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise

    finally:
        await pipeline.close()


async def main() -> None:
    """Main entry point."""
    # Configuration from environment
    database_url = os.getenv('DATABASE_URL', 'sqlite+aiosqlite:///:memory:')
    csv_filepath = os.getenv('CSV_FILE', 'sample_events.csv')

    logger.info(f"Starting pipeline with database: {database_url}")
    logger.info(f"Processing events from: {csv_filepath}")

    await run_pipeline(database_url, csv_filepath)


if __name__ == '__main__':
    asyncio.run(main())
