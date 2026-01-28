from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import uuid4, UUID

from datetime import datetime

from src.infra.db.models.base_model import Base


class MovieModel(Base):
    __tablename__ = "movie"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True),primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    year: Mapped[str] = mapped_column(String(20), nullable=True)
    imdb_id: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    poster: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

