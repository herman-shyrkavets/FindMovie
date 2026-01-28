from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class MovieCreateDTO:
    """Данные, которые получаем от OMDb (без ID)"""
    title: str
    imdb_id: str
    type: str
    year: str | None = None
    poster: str | None = None


@dataclass(frozen=True)
class MovieDTO:
    """Полная информация о фильме, которую отдаем наружу."""
    title: str
    imdb_id: str
    type: str
    # ВАЖНО: Добавлено = None, чтобы Python не ругался на порядок аргументов
    id: UUID | None = None
    created_at: datetime | None = None
    year: str | None = None
    poster: str | None = None