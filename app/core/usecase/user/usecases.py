from fastapi import HTTPException
from starlette import status

from app.core.config.security.services import AuthService, JWTService
from app.core.usecase.user.adapters import UserUseCaseAdapter
from app.core.usecase.user.inputs import SigninUseCaseInput
from app.core.usecase.user.outputs import LoginUseCaseOutput


class AuthUseCase:
    def __init__(self, auth_service: AuthService, jwt_service: JWTService,
                 user_use_case_adapter: UserUseCaseAdapter) -> None:
        self._auth_service = auth_service
        self._jwt_service = jwt_service
        self._user_use_case_adapter = user_use_case_adapter

    async def sing_in(self, sign_in_input: SigninUseCaseInput):
        return await self._user_use_case_adapter.create_user(sign_in_input)

    async def log_in(self, username: str, password: str):
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
