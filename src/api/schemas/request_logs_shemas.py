from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


class RequestLogCreateShema(BaseModel):
    endpoint: str = Field(..., max_length=250)
    query_parms: str
    result_status: int


class RequestLogShema(BaseModel):
    id: UUID
    endpoint: str = Field(..., max_length=250)
    query_parms: str
    result_status: int
    timestamp: datetime

