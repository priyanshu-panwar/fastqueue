from pydantic import BaseModel
from app.settings import settings


class Queue(BaseModel):
    name: str
    visibility_timeout_seconds: int | None = settings.visibility_timeout_seconds
    max_queue_length: int | None = settings.max_queue_length


class QueueCreate(Queue):
    pass


class QueueUpdate(BaseModel):
    visibility_timeout_seconds: int | None = None
    max_queue_length: int | None = None


class QueueResponse(Queue):
    id: int


class QueueListResponse(BaseModel):
    queues: list[QueueResponse]


class QueueStats(BaseModel):
    VisibleCount: int
    InvisibleCount: int
    DeletedCount: int
