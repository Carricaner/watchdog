from abc import ABC, abstractmethod

from app.core.domain.user.entities import User
from app.core.usecase.object.entities import CreateAnObjectUseCaseInput


class ObjectUseCaseAdapter(ABC):
    @abstractmethod
    async def create_an_object(self, user: User, body: CreateAnObjectUseCaseInput):
        pass
