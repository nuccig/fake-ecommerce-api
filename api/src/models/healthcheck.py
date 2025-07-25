from datetime import datetime

from pydantic import BaseModel  # type: ignore


class HealthResponse(BaseModel):
    response_code: int
    status: str
    message: str
    connection: bool
    timestamp: datetime

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
