from abc import ABC, abstractmethod

from app.core.usecase.user.inputs import SigninUseCaseInput


class UserUseCaseAdapter(ABC):
    @abstractmethod
    async def get_user_by_email(self, email: str):
        pass

    @abstractmethod
    async def create_user(self, sign_in_input: SigninUseCaseInput):
        pass
