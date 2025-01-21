import boto3
from fastapi import UploadFile

from app.core.domain.user.entities import User


class S3Client:
    def __init__(self, aws_access_key: str, aws_secret_key: str, aws_region: str) -> None:
        self._s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region
        )
        self._bucket_name = "project-watchdog"

    async def upload_file(self, user: User, file: UploadFile):
        file_content = await file.read()
        self._s3_client.put_object(
            Bucket=self._bucket_name,
            Key=f"user/{user.id}/{file.filename}",
            Body=file_content,
            ContentType=file.content_type
        )
