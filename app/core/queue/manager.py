import heapq
import time
import threading
from collections import deque
import uuid

from app.core.queue.schemas import Queue
from app.core.message.schemas import (
    SendMessageRequest,
    SendMessageResponse,
    SQSMessage,
    ReceiveMessageResponse,
)


class QueueManager:
    def __init__(self, queue: Queue):
        self.name = queue.name
        self.visibility_timeout_seconds = queue.visibility_timeout_seconds

        self.visible_messages: deque[SQSMessage] = deque()
        self.invisible_heap: list[tuple[float, str, SQSMessage]] = []
        self.receipt_handle_map: dict[str, str] = {}
        self.deleted_receipt_handles: set[str] = set()

        self._lock = threading.Lock()

    def send_message(self, request: SendMessageRequest) -> SendMessageResponse:
        message = SQSMessage(
            Body=request.MessageBody,
            MessageAttributes=request.MessageAttributes,
        )

        if request.DelaySeconds:
            message.VisibilityTimeoutUntil = time.time() + request.DelaySeconds
            heapq.heappush(
                self.invisible_heap,
                (message.VisibilityTimeoutUntil, message.ReceiptHandle, message),
            )
        else:
            message.VisibilityTimeoutUntil = None
            self.visible_messages.append(message)

        return SendMessageResponse(
            MessageId=message.MessageId, MD5OfMessageBody=message.MD5OfBody
        )

    def receive_messages(
        self, max_messages: int = 1, visibility_timeout: int | None = None
    ) -> ReceiveMessageResponse:
        results: list[SQSMessage] = []

        with self._lock:
            while self.visible_messages and len(results) < max_messages:
                message = self.visible_messages.popleft()
                if message.ReceiptHandle in self.deleted_receipt_handles:
                    self.deleted_receipt_handles.discard(message.ReceiptHandle)
                    self.receipt_handle_map.pop(message.ReceiptHandle, None)
                    continue

                message.ApproximateReceiveCount += 1

                message.ReceiptHandle = str(uuid.uuid4())

                expiry = time.time() + (
                    visibility_timeout
                    if visibility_timeout is not None
                    else self.visibility_timeout_seconds
                )
                message.VisibilityTimeoutUntil = expiry

                self.receipt_handle_map[message.ReceiptHandle] = message.MessageId
                heapq.heappush(
                    self.invisible_heap, (expiry, message.ReceiptHandle, message)
                )
                results.append(message)

        return ReceiveMessageResponse(Messages=results)

    def delete_message(self, receipt_handle: str) -> bool:
        with self._lock:
            if receipt_handle in self.receipt_handle_map:
                self.deleted_receipt_handles.add(receipt_handle)
                return True
        return False

    def restore_visible_messages(self):
        now = time.time()

        expired_messages = []
        with self._lock:
            while self.invisible_heap and self.invisible_heap[0][0] <= now:
                expired_messages.append(heapq.heappop(self.invisible_heap))

        messages_to_restore = []
        handles_to_cleanup = []

        for expiry, receipt_handle, message in expired_messages:
            if receipt_handle not in self.deleted_receipt_handles:
                message.VisibilityTimeoutUntil = None
                messages_to_restore.append(message)
            else:
                handles_to_cleanup.append(receipt_handle)

        if messages_to_restore or handles_to_cleanup:
            with self._lock:
                self.visible_messages.extend(messages_to_restore)

                for handle in handles_to_cleanup:
                    self.deleted_receipt_handles.discard(handle)
                    self.receipt_handle_map.pop(handle, None)
