def load_queues():
    """
    Load all queues from the database.
    """
    from app.core.queue.models import Queue
    from app.core.queue.registry import QueueRegistry
    from app.database import SessionLocal

    db = SessionLocal()
    queues = db.query(Queue).all()
    db.close()
    for queue in queues:
        QueueRegistry.add_queue(queue)
    return queues
