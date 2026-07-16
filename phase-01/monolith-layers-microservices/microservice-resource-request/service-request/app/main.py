from fastapi import FastAPI

from app.routers.health import router as health_router
from app.routers.requests import router as requests_router

app = FastAPI(
    description="Receives resource requests and stores them in a database for processing.",
    version="1.0.0",
    title="Resource Request Service"
)

app.include_router(health_router)
app.include_router(requests_router)