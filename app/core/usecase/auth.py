from pydantic import BaseModel
from starlette import status
from fastapi import HTTPException

from app.core.config.security.services import AuthService, JWTService


class LoginUseCaseOutput(BaseModel):
    success: bool = False
    token: str = ""


class AuthUseCase:
    def __init__(self, auth_service: AuthService, jwt_service: JWTService) -> None:
        self._auth_service = auth_service
        self._jwt_service = jwt_service

    async def login(self, username: str, password: str):
        authenticated = await self._auth_service.authenticate_user(username, password)
        if not authenticated:
            return LoginUseCaseOutput()
        payload = {
            "sub": username
        }
        return LoginUseCaseOutput(success=True, token=self._jwt_service.encode(payload))

    def get_current_user(self, token: str):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        response = self._jwt_service.decode(token)
        if not response.success:
            raise credentials_exception
        return response.payload

