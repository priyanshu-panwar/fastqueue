from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.queue.schemas import (
    QueueCreate,
    QueueUpdate,
    QueueResponse,
    QueueListResponse,
)
from app.core.queue import service
from app.core.queue.exceptions import (
    QueueAlreadyExistsException,
    QueueNotFoundException,
)
from app.auth.service import verify_api_key
from app.auth2.dependencies import get_current_user

router = APIRouter(
    prefix="/queues", tags=["queues"], dependencies=[Depends(get_current_user)]
)


@router.post(
    "",
    response_model=QueueResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new queue",
)
def create_queue(queue: QueueCreate, db: Session = Depends(get_db)):
    try:
        return service.create_queue(db, queue)
    except QueueAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Queue with the given name already exists.",
        )


@router.delete(
    "/{name}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a queue by name",
)
def delete_queue(name: str, db: Session = Depends(get_db)):
    try:
        service.delete_queue(db, name)
    except QueueNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Queue not found.",
        )


@router.get(
    "",
    response_model=QueueListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all queues",
)
def list_queues(db: Session = Depends(get_db)):
    queues = service.get_all_queues(db)
    return {"queues": queues}


@router.patch(
    "/{name}",
    response_model=QueueResponse,
    status_code=status.HTTP_200_OK,
    summary="Update queue config",
)
def update_queue(name: str, queue_update: QueueUpdate, db: Session = Depends(get_db)):
    try:
        return service.update_queue(db, name, queue_update)
    except QueueNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Queue not found.",
        )
