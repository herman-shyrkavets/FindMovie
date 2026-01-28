from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app_layer.interfaces import IMovieRepository
from src.domain.entities import MovieEntity
from src.infra.db.models.movie_model import MovieModel


class MovieRepository(IMovieRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    def _model_to_entity(self, model: MovieModel) -> MovieEntity:
        return MovieEntity(
            id=model.id,
            title=model.title,
            year=model.year,
            imdb_id=model.imdb_id,
            type=model.type,
            poster=model.poster,
            created_at=model.created_at,
        )

    async def add_movie(self, movie: MovieEntity) -> MovieEntity:
        movie_model = MovieModel(
            title=movie.title,
            year=movie.year,
            imdb_id=movie.imdb_id,
            type=movie.type,
            poster=movie.poster,
        )
        self._session.add(movie_model)
        await self._session.commit()
        await self._session.refresh(movie_model)
        return self._model_to_entity(movie_model)

    async def get_movie_by_imdb_id(self, imdb_id: str) -> MovieEntity | None:
        stmt = select(MovieModel).where(MovieModel.imdb_id == imdb_id)
        result = await self._session.execute(stmt)
        db_movie = result.scalar_one_or_none()
        if db_movie is None:
            return None
        return self._model_to_entity(db_movie)

    async def get_movie_by_title(self, title: str) -> MovieEntity | None:
        stmt = select(MovieModel).where(MovieModel.title == title)
        result = await self._session.execute(stmt)
        db_movie = result.scalar_one_or_none()
        if db_movie is None:
            return None
        return self._model_to_entity(db_movie)

    async def list(self, skip: int = 0, limit: int = 10) -> list[MovieEntity]:
        stmt = select(MovieModel).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        models = result.scalars().all()

        return [self._model_to_entity(model) for model in models]