from abc import ABC, abstractmethod

from fastapi import UploadFile

from app.core.domain.user.entities import User


class ObjectUseCaseAdapter(ABC):
    @abstractmethod
    async def create_a_file(self, user: User, file: UploadFile):
        pass
