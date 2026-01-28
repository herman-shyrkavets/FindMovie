from src.app_layer.interfaces import IMovieRepository, IMovieClient
from src.app_layer.dto.movie_dto import MovieDTO
from src.domain.entities import MovieEntity


class MovieService:
    def __init__(self, movie_repo: IMovieRepository, movie_client: IMovieClient):
        self.movie_repo = movie_repo
        self.movie_client = movie_client


    def _entity_to_dto(self, entity: MovieEntity) -> MovieDTO:
        """Конвертер из внутренней Сущности в DTO для ответа"""
        return MovieDTO(
            id=entity.id,
            title=entity.title,
            imdb_id=entity.imdb_id,
            type=entity.type,
            created_at=entity.created_at,
            year=entity.year,
            poster=entity.poster,
        )


    async def get_movie(self, title: str) ->  MovieDTO | None:
        movie_entity = await self.movie_repo.get_movie_by_title(title)

        if movie_entity:
            return self._entity_to_dto(movie_entity)

        external_movie_dto = await self.movie_client.search_movie(title)

        if not external_movie_dto:
            return None

        new_entity = MovieEntity(
            id=None,
            created_at=None,
            title=external_movie_dto.title,
            imdb_id=external_movie_dto.imdb_id,
            type=external_movie_dto.type,
            year=external_movie_dto.year,
            poster=external_movie_dto.poster,
        )

        saved_entity = await self.movie_repo.add_movie(new_entity)

        return self._entity_to_dto(saved_entity)


    async def list_movies(self, skip: int = 0, limit: int = 10) -> list[MovieDTO]:
        movies = await self.movie_repo.list(skip, limit)
        return[self._entity_to_dto(movie) for movie in movies]


    async def get_movie_by_imdb_id(self, imdb_id: str) -> MovieDTO | None:
        movie = await self.movie_repo.get_movie_by_imdb_id(imdb_id)
        if movie:
            return self._entity_to_dto(movie)
        return None





