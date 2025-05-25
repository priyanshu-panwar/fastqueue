from typing import Optional
from .models import Queue


# Global in-memory store for all queues
class QueueRegistry:
    _queues: dict[str, Queue] = {}

    @classmethod
    def add_queue(cls, queue: Queue):
        cls._queues[queue.name] = queue

    @classmethod
    def get_queue(cls, name: str) -> Optional[Queue]:
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
