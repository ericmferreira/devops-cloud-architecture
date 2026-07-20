from fastapi import FastAPI
from contextlib import asynccontextmanager
## FAST API ROUTERS
from app.routers.health import router as health_router
from app.routers.requests import router as requests_router
## SQL ALCHEMY
from app.database import Base, engine
from app.models.request import Request
from app.routers.requests import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    description="Receives resource requests and stores them in a database for processing.",
    version="1.0.0",
    title="Resource Request Service",
    lifespan=lifespan
)

app.include_router(health_router)
app.include_router(requests_router)