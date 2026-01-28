from uuid import uuid4
from datetime import datetime

from src.app_layer.dto.request_logs_dto import RequestLogCreateDTO
from src.app_layer.interfaces import IRequestLogRepository
from src.domain.entities import RequestLogEntity


class RequestLogsService:
    def __init__(self, log_repo: IRequestLogRepository):
        self.log_repo = log_repo

    async def record_log(self, log_dto: RequestLogCreateDTO) -> None:
        log_entity = RequestLogEntity(
            id=uuid4(),
            endpoint=log_dto.endpoint,
            query_params=log_dto.query_params,
            result_status=log_dto.result_status,
            timestamp=datetime.utcnow()
        )

        await self.log_repo.add_log(log_entity)

