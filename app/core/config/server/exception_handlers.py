from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.responses import Response

from app.core.config.server.entities import StandardErrorResponseEntity
from app.core.config.server.error_codes import ErrorCode


async def validation_exception_handler(request, exc) -> Response:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=StandardErrorResponseEntity(
            error_code=ErrorCode.ENTITY_INVALIDATION.value, message=exc.errors()
        ).model_dump()
    )


async def http_exception_handler(request, exc) -> Response:
    headers = getattr(exc, "headers", None)
    return JSONResponse(
        status_code=exc.status_code,
        headers=headers,
        content=StandardErrorResponseEntity(
            error_code=ErrorCode.GENERAL_HTTP.value, message=exc.detail
        ).model_dump()
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=StandardErrorResponseEntity(
            error_code=500, message=str(exc)
        ).dict()
    )


exception_handler_mapping_dict = {
    RequestValidationError: validation_exception_handler,
    StarletteHTTPException: http_exception_handler,
    Exception: generic_exception_handler
}

__all__ = [
    "exception_handler_mapping_dict"
]
