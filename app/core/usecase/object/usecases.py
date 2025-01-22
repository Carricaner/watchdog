from fastapi import UploadFile

from app.core.domain.user.entities import User
from app.core.usecase.object.adapters import ObjectUseCaseAdapter


class ObjectUseCase:
    def __init__(self, object_use_case_adapter: ObjectUseCaseAdapter) -> None:
        self._object_use_case_adapter = object_use_case_adapter

    async def initialize_watchdog_storage(self):
        lifecycle_policy_exists = await self._object_use_case_adapter.lifecycle_policy_exits()
        if not lifecycle_policy_exists:
            await self._object_use_case_adapter.update_lifecycle_policy()

    async def create_a_file(self, user: User, file: UploadFile):
        await self._object_use_case_adapter.create_a_file(user, file)
