import logging
from fastapi import FastAPI

from app.events.lifespan import lifespan
from app.router.api import router as api_router
from app.database import Base, engine
from app.settings import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastQueue REST APIs",
    description="A fast, lightweight, open-source SQS alternative.",
    version="0.1.0",
    lifespan=lifespan,
)

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)


@app.get("/health", tags=["health"])
async def health_check():
    return {"message": "FastQueue is running!"}


app.include_router(api_router)
