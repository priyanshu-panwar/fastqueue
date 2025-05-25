import asyncio
import logging

from app.core.queue.registry import QueueRegistry
from app.settings import settings

_logger = logging.getLogger(__name__)


async def restore_loop():
    _logger.info("Starting async background queue messages restore loop.")
    while True:
        queues = QueueRegistry.all_queues()
        for queue in queues.values():
            queue.restore_visible_messages()
        await asyncio.sleep(settings.restore_interval_ms / 1000)
