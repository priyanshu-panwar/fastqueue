import logging

from sqlalchemy.orm import Session

from app.core.queue.models import Queue
from app.core.queue.schemas import QueueCreate, QueueUpdate, QueueResponse
from app.core.queue.registry import QueueRegistry
from app.core.queue.exceptions import *


_logger = logging.getLogger(__name__)


def create_queue(db: Session, queue_data: QueueCreate) -> QueueResponse:
    # Check if queue already exists in DB
    existing = QueueRegistry.exists(queue_data.name)
    if existing:
        _logger.warning(f"Queue {queue_data.name} already exists in registry")
        raise QueueAlreadyExistsException()

    # Create DB record
    try:
        db_queue = Queue(**queue_data.model_dump())
        db.add(db_queue)
        db.commit()
        db.refresh(db_queue)
    except Exception as e:
        db.rollback()
        _logger.error(f"Failed to create queue {queue_data.name}: {e}")
        raise QueueCreationException()

    # Register in in-memory registry
    QueueRegistry.add_queue(db_queue)

    _logger.info(f"Queue {queue_data.name} created successfully")

    return QueueResponse.model_validate(db_queue, from_attributes=True)


def delete_queue(db: Session, queue_name: str) -> None:
    # Check if queue exists in DB
    queue = db.query(Queue).filter_by(name=queue_name).first()
    if not queue:
        _logger.warning(f"Queue {queue_name} not found in DB")
        raise QueueNotFoundException()

    # Delete from DB
    db.delete(queue)
    db.commit()

    # Remove from registry
    QueueRegistry.delete_queue(queue_name)

    _logger.info(f"Queue {queue_name} deleted successfully")


def get_all_queues(db: Session) -> list[QueueResponse]:
    queues = db.query(Queue).all()
    return [QueueResponse.model_validate(q, from_attributes=True) for q in queues]


def update_queue(db: Session, name: str, update_data: QueueUpdate) -> QueueResponse:
    queue = db.query(Queue).filter_by(name=name).first()
    if not queue:
        _logger.warning(f"Queue {name} not found in DB")
        raise QueueNotFoundException()

    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(queue, field, value)

    db.commit()
    db.refresh(queue)

    _logger.info(f"Queue {name} updated successfully")

    return QueueResponse.model_validate(queue, from_attributes=True)


def get_queue_by_name(db: Session, name: str) -> QueueResponse | None:
    queue = db.query(Queue).filter_by(name=name).first()
    if not queue:
        _logger.warning(f"Queue {name} not found in DB")
        return None

    return QueueResponse.model_validate(queue, from_attributes=True)
