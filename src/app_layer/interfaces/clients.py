from abc import ABC, abstractmethod
from src.app_layer.dto.movie_dto import MovieCreateDTO

class IMovieClient(ABC):
    @abstractmethod
    async def search_movie(self, title: str) -> MovieCreateDTO | None:
        """Ищет фильм во внешней системе. Возвращает DTO для создания (без ID) или None, если фильм не найден."""
        pass