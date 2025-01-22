from typing import List

from fastapi import UploadFile

from app.core.domain.user.entities import User
from app.core.usecase.object.adapters import ObjectUseCaseAdapter
from app.external.aws.s3 import S3Client
from app.external.database.mongodb.managers import MongodbManager


class ObjectUseCaseAdapterImpl(ObjectUseCaseAdapter):

    def __init__(self, mongodb_manager: MongodbManager, s3_client: S3Client) -> None:
        self._mongodb_manager = mongodb_manager
        self._s3_client = s3_client

    async def lifecycle_policy_exits(self) -> bool:
        return await self._s3_client.lifecycle_policy_exists()

    async def update_lifecycle_policy(self) -> None:
        await self._s3_client.overwrite_lifecycle_policy()

    async def create_a_file(self, user: User, file: UploadFile):
        await self._s3_client.upload_file(user, file)

    async def get_all_user_files(self, user: User) -> List[str]:
        return await self._s3_client.list_all_file_names(user)

    async def file_exists(self, user: User, file_name: str):
        return await self._s3_client.file_exist(user, file_name)

    async def create_presigned_url(self, user: User, file_name: str, expiration_in_seconds: int = 3600) -> str:
        return await self._s3_client.create_presigned_url(user, file_name, expiration_in_seconds)
