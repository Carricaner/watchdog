from fastapi import FastAPI, APIRouter

from app.core.config.server.parameters import fastapi_parameters, main_router_parameters

app = FastAPI(**fastapi_parameters)

main_router = APIRouter(
    **main_router_parameters
)


@main_router.get("/demo")
async def root():
    return {"message": "Hello World"}


app.include_router(main_router)
