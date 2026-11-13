from fastapi import FastAPI

from app.api.tasks import router

app = FastAPI(
    title="Senior Task Brick",
    description="Isolated, strictly typed task management service.",
    version="1.0.0",
)
app.include_router(router)
