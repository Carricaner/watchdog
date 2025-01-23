from app.core.config.security.services import JWTService, BcryptService
from app.core.usecase.user.adapters import UserUseCaseAdapter
from app.core.usecase.user.entities import SigninUseCaseInput, LoginUseCaseOutput


class AuthUseCase:
    def __init__(self, jwt_service: JWTService,
                 user_use_case_adapter: UserUseCaseAdapter, hash_service: BcryptService) -> None:
        self._jwt_service = jwt_service
        self._user_use_case_adapter = user_use_case_adapter
        self._hash_service = hash_service

    async def sing_in(self, sign_in_input: SigninUseCaseInput) -> True:
        user = await self._user_use_case_adapter.get_user_by_email(sign_in_input.email)
        if user:
            raise Exception("Email already existed.")
        return await self._user_use_case_adapter.create_user(sign_in_input)

    async def log_in(self, email: str, password: str):
        user = await self._user_use_case_adapter.get_user_by_email(email)
        if not user or user.disabled or not self._hash_service.verify(password, user.password):
            return LoginUseCaseOutput()
        payload = {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "disabled": user.disabled
        }
        return LoginUseCaseOutput(success=True, token=self._jwt_service.encode(payload))
