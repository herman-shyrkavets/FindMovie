import logging
import aiohttp
from src.app_layer.dto.movie_dto import MovieDTO

logger = logging.getLogger(__name__)


class OmdbClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://www.omdbapi.com/"

    async def search_movie(self, title: str) -> MovieDTO | None:
        params = {"apikey": self.api_key, "t": title}

        logger.info(f"Запрос к OMDb API. Фильм: '{title}', Ключ (первые 3 симв.): {self.api_key[:3]}***")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status != 200:
                        logger.error(f"OMDb вернул HTTP {response.status}")
                        return None

                    data = await response.json()

                    logger.info(f"Ответ от OMDb: {data}")

            if data.get("Response") == "False":
                error_msg = data.get("Error")
                logger.warning(f"OMDb не нашел фильм. Ошибка API: {error_msg}")
                return None

            logger.info("Фильм успешно найден и распаршен.")

            return MovieDTO(
                title=data.get("Title"),
                year=data.get("Year"),
                imdb_id=data.get("imdbID"),
                type=data.get("Type"),
                poster=data.get("Poster") if data.get("Poster") != "N/A" else None,
                created_at=None
            )

        except Exception as e:
            logger.exception(f"Критическая ошибка при запросе к OMDb: {e}")
            return None