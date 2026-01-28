from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class MovieCreateSchema(BaseModel):
    title: str = Field(...,min_length=1, max_length=250)
    imdb_id: str = Field(...,min_length=1, max_length=20)
    type: str = Field(...,min_length=1, max_length=50)
    year:str = Field(...,min_length=1, max_length=20)
    poster: str | None = Field(None, max_length=500)

class MovieSchema(BaseModel):
    id: UUID
    title: str = Field(..., min_length=1, max_length=250)
    imdb_id: str = Field(..., min_length=1, max_length=20)
    type: str = Field(..., min_length=1, max_length=50)
    year: str = Field(..., min_length=1, max_length=20)
    poster: str | None = Field(None, max_length=500)
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

