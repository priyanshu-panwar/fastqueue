from sqlalchemy import Column, String, Integer

from app.settings import settings
from app.database import Base


class Queue(Base):
    __tablename__ = "queues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    visibility_timeout_seconds = Column(
        Integer, default=settings.visibility_timeout_seconds
    )
    max_queue_length = Column(Integer, default=settings.max_queue_length)
