from fastapi import HTTPException
from starlette import status

from app.core.config.security.services import JWTService, BcryptService
from app.core.usecase.user.adapters import UserUseCaseAdapter
from app.core.usecase.user.inputs import SigninUseCaseInput
from app.core.usecase.user.outputs import LoginUseCaseOutput


class AuthUseCase:
    def __init__(self, jwt_service: JWTService,
                 user_use_case_adapter: UserUseCaseAdapter, hash_service: BcryptService) -> None:
        self._jwt_service = jwt_service
        self._user_use_case_adapter = user_use_case_adapter
        self._hash_service = hash_service

    async def sing_in(self, sign_in_input: SigninUseCaseInput):
        # TODO need to check if the email exists or not
        return await self._user_use_case_adapter.create_user(sign_in_input)

    async def log_in(self, email: str, password: str):
        user = await self._user_use_case_adapter.get_user_by_email(email)
        if not user or not self._hash_service.verify(password, user.password):
            return LoginUseCaseOutput()
        payload = {
            "sub": user.username,
            "email": email
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
