from abc import ABC, abstractmethod

from fastapi import UploadFile

from app.core.domain.user.entities import User


class ObjectUseCaseAdapter(ABC):
    @abstractmethod
    async def lifecycle_policy_exits(self) -> bool:
        pass

    @abstractmethod
    async def update_lifecycle_policy(self) -> None:
        pass

    @abstractmethod
    async def create_a_file(self, user: User, file: UploadFile):
        pass

    @abstractmethod
    async def get_all_user_files(self, user: User):
        pass
