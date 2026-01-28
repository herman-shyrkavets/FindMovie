from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from src.infra.db.session import async_session_factory
from src.infra.repositories.request_log_repository import RequestLogRepository
from src.app_layer.use_cases.request_logs_service import RequestLogsService
from src.app_layer.dto.request_logs_dto import RequestLogCreateDTO


class RequestLogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if request.url.path in ["/docs", "/openapi.json", "/favicon.ico"]:
            return response

        try:
            async with async_session_factory() as session:
                repo = RequestLogRepository(session)
                service = RequestLogsService(log_repo=repo)

                log_dto = RequestLogCreateDTO(
                    endpoint=request.url.path,
                    query_params=str(request.query_params),
                    result_status=response.status_code
                )
                await service.record_log(log_dto)

        except Exception as e:
            print(f"FAILED TO LOG REQUEST: {e}")

        return response