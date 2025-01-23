from typing import List

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

    async def create_a_file(self, user: User, file: UploadFile) -> None:
        await self._object_use_case_adapter.create_a_file(user, file)

    async def get_all_user_files(self, user: User) -> List[str]:
        return await self._object_use_case_adapter.get_all_user_files(user)

    async def create_presigned_url(self, user: User, file_name: str, expiration_in_seconds: int = 3600):
        if file_name is None or not file_name.strip():
            raise ValueError("The file name must not be None or empty.")
        file_name = file_name.strip()
        file_exists = await self._object_use_case_adapter.file_exists(user, file_name)
        if not file_exists:
            raise Exception(f'The file with name of {file_name} does not exist.')
        return await self._object_use_case_adapter.create_presigned_url(user, file_name, expiration_in_seconds)
