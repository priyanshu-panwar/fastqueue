import heapq
import time
import threading
from collections import deque

from app.core.queue.schemas import Queue
from app.core.message.schemas import (
    SendMessageRequest,
    SendMessageResponse,
    SQSMessage,
    ReceiveMessageResponse,
    DeleteMessageRequest,
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
        else:
            message.VisibilityTimeoutUntil = None

        # with self._lock:
        self.visible_messages.append(message)

        return SendMessageResponse(
            MessageId=message.MessageId, MD5OfMessageBody=message.MD5OfBody
        )

    def receive_messages(self, max_messages: int = 1) -> ReceiveMessageResponse:
        results: list[SQSMessage] = []

        with self._lock:
            while self.visible_messages and len(results) < max_messages:
                message = self.visible_messages.popleft()
                if message.ReceiptHandle in self.deleted_receipt_handles:
                    continue

                expiry = time.time() + (
                    self.visibility_timeout_seconds
                    if self.visibility_timeout_seconds is not None
                    else 0
                )

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
        # with self._lock:
        while self.invisible_heap and self.invisible_heap[0][0] <= now:
            _, receipt_handle, message = heapq.heappop(self.invisible_heap)
            if receipt_handle not in self.deleted_receipt_handles:
                self.visible_messages.append(message)
            else:
                self.deleted_receipt_handles.discard(receipt_handle)
                self.receipt_handle_map.pop(receipt_handle, None)
