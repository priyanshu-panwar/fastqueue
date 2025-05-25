import logging

_logger = logging.getLogger(__name__)


def load_queues():
    """
    Load all queues from the database.
    """
    from app.core.queue.models import Queue
    from app.core.queue.schemas import Queue as QueueSchema
    from app.core.queue.registry import QueueRegistry
    from app.database import SessionLocal

    db = SessionLocal()
    queues = db.query(Queue).all()
    db.close()
    for queue in queues:
        QueueRegistry.add_queue(QueueSchema.model_validate(queue, from_attributes=True))
        _logger.info(f"Queue {queue.name} loaded into registry")
    _logger.info(f"Total queues loaded: {len(queues)}")
    return queues
