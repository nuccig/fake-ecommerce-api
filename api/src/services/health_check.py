from datetime import datetime

from ..models.healthcheck import HealthResponse


class HealthService:
    @staticmethod
    def get_health_status() -> HealthResponse:
        return HealthResponse(
            status="healthy", message="API is running", timestamp=datetime.now()
        )
