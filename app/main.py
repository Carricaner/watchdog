from fastapi import FastAPI, APIRouter

from app.core.config.server.parameters import fastapi_parameters, main_router_parameters
from app.entry.restful.routers import objects

app = FastAPI(**fastapi_parameters)

main_router = APIRouter(
    **main_router_parameters
)

main_router.include_router(objects.router)

app.include_router(main_router)
