from fastapi import APIRouter  # type: ignore

from .health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router, prefix="/api/v1")
