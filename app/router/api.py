from fastapi import APIRouter
from app.router.queue import router as queue_router
from app.router.message import router as message_router
from app.router.auth2 import router as auth_router


router = APIRouter(prefix="/v1")
router.include_router(queue_router)
router.include_router(message_router)
router.include_router(auth_router)
