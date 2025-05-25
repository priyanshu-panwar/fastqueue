from typing import Optional
from .schemas import Queue
from .manager import QueueManager


# Global in-memory store for all queues
class QueueRegistry:
    _queues: dict[str, QueueManager] = {}

    @classmethod
    def add_queue(cls, queue: Queue):
        if cls.exists(queue.name):
            raise ValueError(f"Queue with name '{queue.name}' already exists.")
        cls._queues[queue.name] = QueueManager(queue)

    @classmethod
    def get_queue(cls, name: str) -> Optional[QueueManager]:
        if cls.exists(name):
            return cls._queues[name]
        return None

    @classmethod
    def delete_queue(cls, name: str):
        cls._queues.pop(name, None)

    @classmethod
    def exists(cls, name: str) -> bool:
        return name in cls._queues

    @classmethod
    def all_queues(cls) -> dict[str, Queue]:
        return cls._queues
