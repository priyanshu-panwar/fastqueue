import heapq
import time
import uuid
import threading
from collections import deque

from app.core.message.schemas import Message
from app.core.queue.schemas import Queue


class QueueManager:
    def __init__(self, queue: Queue):
        self.name = queue.name
        self.visibility_timeout_seconds = queue.visibility_timeout_seconds

        self.visible_messages: deque[Message] = deque()
        self.invisible_heap: list[tuple[float, str, Message]] = []
        self.receipt_handle_map: dict[str, str] = {}
        self.deleted_receipt_handles: set[str] = set()

        self._lock = threading.Lock()

    def enqueue(self, message: Message):
        with self._lock:
            self.visible_messages.append(message)

    def dequeue(self) -> tuple[Message, str] | None:
        with self._lock:
            if not self.visible_messages:
                return None

            message = self.visible_messages.popleft()
            message.received_at = time.time()

            # Generate a receipt handle
            receipt_handle = self._generate_receipt_handle()
            self.receipt_handle_map[receipt_handle] = message.id

            # Set visibility timeout
            visibility_expiry = time.time() + self.visibility_timeout_seconds
            heapq.heappush(
                self.invisible_heap, (visibility_expiry, receipt_handle, message)
            )

            return message, receipt_handle

    def delete_message(self, receipt_handle: str):
        with self._lock:
            if receipt_handle in self.receipt_handle_map:
                self.deleted_receipt_handles.add(receipt_handle)

    def is_deleted(self, receipt_handle: str) -> bool:
        with self._lock:
            return receipt_handle in self.deleted_receipt_handles

    def restore_visible_messages(self):
        now = time.time()
        with self._lock:
            while self.invisible_heap and self.invisible_heap[0][0] <= now:
                _, receipt_handle, message = heapq.heappop(self.invisible_heap)
                if receipt_handle not in self.deleted_receipt_handles:
                    self.visible_messages.append(message)
                else:
                    self.deleted_receipt_handles.discard(receipt_handle)
                    self.receipt_handle_map.pop(receipt_handle, None)

    def _generate_receipt_handle(self) -> str:
        return str(uuid.uuid4())
