from abc import ABC, abstractmethod

from app.core.domain.user.entities import User
from app.core.usecase.user.entities import SigninUseCaseInput


class UserUseCaseAdapter(ABC):
    @abstractmethod
    async def get_user_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    async def create_user(self, sign_in_input: SigninUseCaseInput):
        pass
