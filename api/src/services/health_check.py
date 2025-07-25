from datetime import datetime

from sqlalchemy import text  # type: ignore

from ..core.database import engine
from ..models.healthcheck import HealthResponse


class HealthService:
    @staticmethod
    def get_health_status() -> HealthResponse:
        try:

            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))

            return HealthResponse(
                response_code=200,
                status="healthy",
                message="API rodando e banco conectado",
                connection=True,
                timestamp=datetime.now(),
            )
        except Exception as e:
            return HealthResponse(
                response_code=503,
                status="unhealthy",
                message=f"Falha na conexão com o banco de dados: {str(e)}",
                connection=False,
                timestamp=datetime.now(),
            )
