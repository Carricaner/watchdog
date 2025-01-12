from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from app.core.config.di.containers import CoreContainer
from app.core.config.security.services import JWTService

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
):
    response = jwt_service.decode(token)
    if not response.success:
        raise credentials_exception
    return response.payload
