import json
from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from app.core.config.di.containers import CoreContainer
from app.core.config.security.services import JWTService
from app.core.domain.user.entities import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/auth")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


@inject
def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        jwt_service: JWTService = Depends(Provide[CoreContainer.jwt_service])
) -> User:
    response = jwt_service.decode(token)
    if not response.success:
        raise credentials_exception
    return User(**response.payload)


class UnifiedResponseMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        response: Response = await call_next(request)
        body = b"".join([chunk async for chunk in response.body_iterator])
        original_data = json.loads(body.decode("utf-8"))
        wrapped_data = {
            "code": 0,
            "msg": "success",
            "data": original_data,
        }
        return JSONResponse(content=wrapped_data)
