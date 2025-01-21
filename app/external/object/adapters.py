from fastapi import UploadFile

from app.core.domain.user.entities import User
from app.core.usecase.object.adapters import ObjectUseCaseAdapter
from app.external.aws.s3 import S3Client
from app.external.database.mongodb.managers import MongodbManager


class ObjectUseCaseAdapterImpl(ObjectUseCaseAdapter):

    def __init__(self, mongodb_manager: MongodbManager, s3_client: S3Client) -> None:
        self._mongodb_manager = mongodb_manager
        self._s3_client = s3_client

    async def create_a_file(self, user: User, file: UploadFile):
        await self._s3_client.upload_file(user, file)
