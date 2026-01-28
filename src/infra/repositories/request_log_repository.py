from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.app_layer.interfaces import IRequestLogRepository
from src.domain.entities import RequestLogEntity
from src.infra.db.models.request_log_model import RequestLogModel


class RequestLogRepository(IRequestLogRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    def _model_to_entity(self, model: RequestLogModel) -> RequestLogEntity:
        return RequestLogEntity(
            id=model.id,
            endpoint=model.endpoint,
            query_params=model.query_params,
            result_status=model.result_status,
            timestamp=model.timestamp,
        )

    async def add_log(self, log: RequestLogEntity) -> RequestLogEntity:
        log_model = RequestLogModel(
            id=log.id,
            endpoint=log.endpoint,
            query_params=log.query_params,
            result_status=log.result_status,
            timestamp=log.timestamp
        )
        self._session.add(log_model)
        await self._session.commit()
        return self._model_to_entity(log_model)

    async def list(self, skip: int = 0, limit: int = 50) -> list[RequestLogEntity]:
        stmt = (
            select(RequestLogModel)
            .order_by(desc(RequestLogModel.timestamp))
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        models = result.scalars().all()
        return [self._model_to_entity(model) for model in models]