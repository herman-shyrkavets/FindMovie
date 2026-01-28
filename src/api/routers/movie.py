from fastapi import APIRouter, Depends, HTTPException, Query, status
from dependency_injector.wiring import Provide, inject

from src.depends import Container
from src.api.schemas.movie_schemas import MovieSchema
from src.app_layer.use_cases import MovieService
router = APIRouter()

@router.get(
    "/search",
    response_model=MovieSchema,
    summary="Get movie",
    responses={
        400: {"description": "Bad Request"},
    }
)
@inject
async def search_movie(
        title: str = Query(..., min_length=1, max_length=250, description="Название фильма для поиска"),
        service: MovieService = Depends(Provide[Container.use_case.movie_service])
):
    movie = await service.get_movie(title)

    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Фильм '{title}' не найден ни в базе, ни в OMDb"
        )

    return movie

@router.get("/", response_model=list[MovieSchema])
@inject
async def list_movies(
    skip: int = 0,
    limit: int = 10,
    service: MovieService = Depends(Provide[Container.use_case.movie_service])
):
    return await service.list_movies(skip, limit)



@router.get("/{imdb_id}", response_model=MovieSchema)
@inject
async def get_movie_by_id(
        imdb_id: str,
        service: MovieService = Depends(Provide[Container.use_case.movie_service])
):

    movie = await service.get_movie_by_imdb_id(imdb_id)

    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Фильм не найден"
        )

    return movie



