import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.routers import classify, export, health, models_router, tickets


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    logging.basicConfig(
        level=getattr(logging, get_settings().log_level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger(__name__)
    logger.info(
        "Starting %s v%s", get_settings().app_title, get_settings().app_version
    )
    yield
    logger.info("Shutting down")


app = FastAPI(
    title=get_settings().app_title,
    version=get_settings().app_version,
    lifespan=lifespan,
)


app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", include_in_schema=False)
async def root() -> FileResponse:
    return FileResponse("app/static/index.html")


app.include_router(classify.router)
app.include_router(health.router)
app.include_router(models_router.router)
app.include_router(tickets.router)
app.include_router(export.router)
