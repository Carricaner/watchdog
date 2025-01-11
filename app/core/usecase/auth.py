from pydantic import BaseModel

from app.core.config.security.services import AuthService, JWTService


class LoginUseCaseOutput(BaseModel):
    success: bool = False
    token: str = ""


class AuthUseCase:
    def __init__(self, auth_service: AuthService, jwt_service: JWTService) -> None:
        self._auth_service = auth_service
        self._jwt_service = jwt_service

    def login(self, username: str, password: str):
        authenticated = self._auth_service.authenticate_user(username, password)
        if not authenticated:
            return LoginUseCaseOutput()
        payload = {
            "sub": username
        }
        return LoginUseCaseOutput(success=True, token=self._jwt_service.encode(payload))
