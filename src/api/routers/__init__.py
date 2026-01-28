from fastapi import APIRouter

from src.api.routers.movie import router as movie_router

router = APIRouter()

router.include_router(
    movie_router,
    prefix="/movies",
    tags=["Movies"]
)