from abc import ABC, abstractmethod

from src.domain.entities import MovieEntity


class IMovieRepository(ABC):
    @abstractmethod
    async def add_movie(self, movie: MovieEntity) -> MovieEntity:
        pass

    @abstractmethod
    async def get_movie_by_imdb_id(self, imdb_id: str) -> MovieEntity | None:
        pass

    @abstractmethod
    async def get_movie_by_title(self, title: str) -> MovieEntity | None:
        pass

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 10) -> list[MovieEntity]:
        pass

