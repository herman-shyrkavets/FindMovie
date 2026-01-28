from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class RequestLogEntity:
    id: UUID
    endpoint: str
    query_params: str | None
    result_status: int
    timestamp: datetime
