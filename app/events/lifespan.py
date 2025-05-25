import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.events.load_queues import load_queues
from app.events.restore_loop import restore_loop
from app.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI application.
    This is used to perform startup and shutdown tasks.
    """
    from app.core.queue.models import Queue

    # Perform startup tasks here
    # Ensure all database tables are created at startup
    Base.metadata.create_all(bind=engine)
    # Load queues from the database
    load_queues()
    # Restore invisible messages in the queue
    asyncio.create_task(restore_loop())

    yield
    # Perform shutdown tasks here
