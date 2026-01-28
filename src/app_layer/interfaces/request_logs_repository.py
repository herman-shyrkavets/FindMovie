from abc import ABC, abstractmethod
from src.domain.entities import RequestLogEntity

class IRequestLogRepository(ABC):
    @abstractmethod
    async def add_log(self, log: RequestLogEntity) -> RequestLogEntity:
        pass

    @abstractmethod
    async def list(self,  skip: int = 0, limit: int = 50) -> list[RequestLogEntity]:
        pass

