import uuid
import time
import hashlib
from pydantic import BaseModel, Field

from app.core.message.enums import SQSAction


class MessageAttributeValue(BaseModel):
    DataType: str  # "String" | "Number" | "Binary"
    StringValue: str | None = None
    BinaryValue: bytes | None = None


class SendMessageRequest(BaseModel):
    Action: SQSAction | None = SQSAction.SendMessage
    MessageBody: str
    DelaySeconds: int | None = 0
    MessageAttributes: dict[str, MessageAttributeValue] | None = None


class SendMessageResponse(BaseModel):
    MessageId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    MD5OfMessageBody: str


class SQSMessage(BaseModel):
    MessageId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    ReceiptHandle: str = Field(default_factory=lambda: str(uuid.uuid4()))
    Body: str
    MD5OfBody: str = ""
    VisibilityTimeoutUntil: float | None = None
    MessageAttributes: dict[str, MessageAttributeValue] | None = None
    ApproximateReceiveCount: int = 0

    def __init__(self, **data):
        super().__init__(**data)
        self.MD5OfBody = hashlib.md5(self.Body.encode("utf-8")).hexdigest()

    def is_visible(self) -> bool:
        return (
            self.VisibilityTimeoutUntil is None
            or self.VisibilityTimeoutUntil <= time.time()
        )


class ReceiveMessageRequest(BaseModel):
    Action: SQSAction | None = SQSAction.ReceiveMessage
    MaxNumberOfMessages: int | None = 1
    VisibilityTimeout: int | None = None
    WaitTimeSeconds: int | None = 0
    MessageAttributeNames: list[str] | None = Field(default_factory=lambda: ["All"])


class ReceiveMessageResponse(BaseModel):
    Messages: list[SQSMessage] | None = Field(default_factory=list)


class DeleteMessageRequest(BaseModel):
    Action: SQSAction | None = SQSAction.DeleteMessage
    ReceiptHandle: str
