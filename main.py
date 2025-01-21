import uvicorn
from fastapi import FastAPI, APIRouter

from app.core.config.security.middlewares import UnifiedResponseMiddleware
from app.core.config.server.exception_handlers import exception_handler_mapping_dict
from app.core.config.server.parameters import fastapi_parameters, main_router_parameters
from app.entry.restful.routers import objects, users

app = FastAPI(**fastapi_parameters)


def register_middlewares(app: FastAPI):
    app.add_middleware(UnifiedResponseMiddleware)


register_middlewares(app)

for exception, exception_handler in exception_handler_mapping_dict.items():
    app.add_exception_handler(exception, exception_handler)

main_router = APIRouter(
    **main_router_parameters
)

main_router.include_router(objects.router)
main_router.include_router(users.router)

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
