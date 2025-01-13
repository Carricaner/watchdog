from app.core.domain.user.entities import User
from app.core.usecase.object.adapters import ObjectUseCaseAdapter
from app.core.usecase.object.entities import CreateAnObjectUseCaseInput


class ObjectUseCase:
    def __init__(self, object_use_case_adapter: ObjectUseCaseAdapter) -> None:
        self._object_use_case_adapter = object_use_case_adapter

    async def create_an_object(self, user: User, body: CreateAnObjectUseCaseInput):
        await self._object_use_case_adapter.create_an_object(user, body)
