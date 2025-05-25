from pydantic import BaseModel


class Queue(BaseModel):
    name: str
    visibility_timeout_seconds: int | None = None
    max_queue_length: int | None = None


class QueueCreate(Queue):
    pass


class QueueUpdate(BaseModel):
    visibility_timeout_seconds: int | None = None
    max_queue_length: int | None = None


class QueueResponse(Queue):
    id: int


class QueueListResponse(BaseModel):
    queues: list[QueueResponse]
