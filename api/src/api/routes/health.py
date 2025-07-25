from fastapi import APIRouter  # type: ignore

from ...models.healthcheck import HealthResponse
from ...services.health_check import HealthService

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthService.get_health_status()
