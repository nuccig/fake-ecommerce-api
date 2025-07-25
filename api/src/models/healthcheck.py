from datetime import datetime

from pydantic import BaseModel  # type: ignore


class HealthResponse(BaseModel):
    status: str
    message: str
    timestamp: datetime

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
