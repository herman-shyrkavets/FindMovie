from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass
class MovieEntity:
    id: UUID |None
    title: str
    year: str
    imdb_id: str
    type: str
    poster: str
    created_at: datetime |None



