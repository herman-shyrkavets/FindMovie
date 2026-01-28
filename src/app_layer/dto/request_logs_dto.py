from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class RequestLogCreateDTO:
    """Данные, которые Middleware собирает о запросе."""
    endpoint: str
    query_params: str
    result_status: int


@dataclass(frozen=True)
class RequestLogDTO:
    """Полный лог для отображения (если понадобится список логов)."""
    id: UUID
    endpoint: str
    query_params: str
    result_status: int
    timestamp: datetime

