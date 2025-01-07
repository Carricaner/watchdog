from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config.server.lifespan_events import application_start, gracefully_shutdown


@asynccontextmanager
async def default_lifespan(app: FastAPI):
    application_start()
    yield
    gracefully_shutdown()
