import uuid
import time
from typing import Optional
from pydantic import BaseModel, Field


class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    body: str
    created_at: float = Field(default_factory=lambda: time.time())
    visibility_timeout_until: Optional[float] = None
    receipt_handle: Optional[str] = None

    def is_visible(self) -> bool:
        """Check if the message is currently visible."""
        return (
            self.visibility_timeout_until is None
            or self.visibility_timeout_until <= time.time()
        )


class SendMessageRequest(BaseModel):
    body: str


class SendMessageResponse(BaseModel):
    message_id: str


class ReceiveMessageResponse(BaseModel):
    message_id: str
    body: str
    receipt_handle: str


class DeleteMessageRequest(BaseModel):
    receipt_handle: str


class QueueStats(BaseModel):
    visible_count: int
    invisible_count: int
    deleted_count: int
