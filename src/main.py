from fastapi import FastAPI

from src.config import settings
from src.depends import create_container
from src.api.routers import router as api_router
from src.api.middlewares.log_middleware import RequestLogMiddleware

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
app = FastAPI(debug=settings.app_settings.debug)

container = create_container(settings)
app.container = container

container.wire(modules=[
    "src.api.routers.movie",
])

app.add_middleware(RequestLogMiddleware)
app.include_router(api_router, prefix="/api/v1")

@app.get("/ht/")
def health_check():
    return {"status": "OK"}
