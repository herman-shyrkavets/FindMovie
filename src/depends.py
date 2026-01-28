from dependency_injector import containers, providers

from src.config import settings
from src.infra.db.session import async_session_factory

from src.app_layer.use_cases import RequestLogsService, MovieService

from src.infra.repositories.movie_repository import MovieRepository
from src.infra.repositories.request_log_repository import RequestLogRepository
from src.infra.clients.omdb_client import OmdbClient


async def get_async_session():
    """
    Открывает сессию, отдает её (yield) и закрывает после использования.
    """
    async with async_session_factory() as session:
        yield session


class DBContainer(containers.DeclarativeContainer):
    session = providers.Resource(get_async_session)


class RepositoryContainer(containers.DeclarativeContainer):
    session = providers.Dependency()

    movie_repository = providers.Factory(
        MovieRepository,
        session=session
    )

    log_repository = providers.Factory(
        RequestLogRepository,
        session=session
    )


# OMDbClient
class GatewayContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    omdb_client = providers.Factory(
        OmdbClient,
        api_key=config.api_key
    )


class UseCaseContainer(containers.DeclarativeContainer):
    movie_repo = providers.Dependency()
    log_repo = providers.Dependency()
    movie_client = providers.Dependency()

    movie_service = providers.Factory(
        MovieService,
        movie_repo=movie_repo,
        movie_client=movie_client
    )

    request_log_service = providers.Factory(
        RequestLogsService,
        log_repo=log_repo
    )


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    db = providers.Container(DBContainer)
    gateways = providers.Container(GatewayContainer,config=config.omdb)
    repositories = providers.Container(RepositoryContainer, session=db.session)
    use_case = providers.Container(UseCaseContainer,
                                   movie_repo=repositories.movie_repository,
                                   log_repo=repositories.log_repository,
                                   movie_client=gateways.omdb_client,
    )


def create_container(settings: settings) -> Container:
    container = Container()
    container.config.from_pydantic(settings)
    return container

