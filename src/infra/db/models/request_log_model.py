from datetime import datetime
from uuid import UUID

from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from src.infra.db.models.base_model import Base


class RequestLogModel(Base):
    __tablename__ = "request_log"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, nullable=False)
    endpoint: Mapped[str] =mapped_column(String(250), nullable=False)
    query_params: Mapped[str | None] = mapped_column(Text, nullable=True)
    result_status: Mapped[int] = mapped_column(Integer, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(server_default=func.now())

