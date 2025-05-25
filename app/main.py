from fastapi import FastAPI

from app.events.lifespan import lifespan
from app.router.api import router as api_router
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastQueue REST APIs",
    description="A fast, lightweight, open-source SQS alternative.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health", tags=["health"])
async def health_check():
    return {"message": "FastQueue is running!"}


app.include_router(api_router)
