from fastapi import APIRouter
from app.router.queue import router as queue_router


router = APIRouter(prefix="/v1")
router.include_router(queue_router)
