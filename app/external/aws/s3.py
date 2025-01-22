from typing import List

import boto3
from botocore.exceptions import ClientError
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
        self._lifecycle_policy_config = {
            'Rules': [
                {
                    'ID': 'WatchDogLifeCyclePolicy',
                    'Status': 'Enabled',
                    'Filter': {
                        'Prefix': ''
                    },
                    'Transitions': [
                        {
                            'Days': 30,
                            'StorageClass': 'STANDARD_IA'
                        },
                        {
                            'Days': 150,
                            'StorageClass': 'GLACIER'
                        }
                    ],
                    'Expiration': {
                        'Days': 250
                    },
                    'NoncurrentVersionExpiration': {
                        'NewerNoncurrentVersions': 5,  # Keep the latest 5 noncurrent versions
                        'NoncurrentDays': 30  # Expire noncurrent versions after 30 days
                    }
                }
            ]
        }

    @staticmethod
    def get_object_prefix(user):
        return f'user/{user.id}/'

    async def upload_file(self, user: User, file: UploadFile):
        file_content = await file.read()
        self._s3_client.put_object(
            Bucket=self._bucket_name,
            Key=f"{self.get_object_prefix(user)}/{file.filename}",
            Body=file_content,
            ContentType=file.content_type
        )

    async def lifecycle_policy_exists(self) -> bool:
        try:
            self._s3_client.get_bucket_lifecycle_configuration(Bucket=self._bucket_name)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
                return False
            else:
                raise Exception(e)

    async def overwrite_lifecycle_policy(self) -> None:
        self._s3_client.put_bucket_lifecycle_configuration(
            Bucket=self._bucket_name,
            LifecycleConfiguration=self._lifecycle_policy_config
        )

    async def list_all_file_names(self, user: User) -> List[str]:
        prefix = self.get_object_prefix(user)
        response = self._s3_client.list_objects_v2(Bucket=self._bucket_name, Prefix=prefix)
        return [obj['Key'].split('/')[-1] for obj in response['Contents']] if 'Contents' in response else []

    async def file_exist(self, user: User, file_name: str) -> bool:
        key = f'{self.get_object_prefix(user)}{file_name}'
        try:
            self._s3_client.head_object(Bucket=self._bucket_name, Key=key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            else:
                raise Exception(e)

    async def create_presigned_url(self, user: User, file_name: str, expiration_in_seconds: int = 3600):
        key = f'{self.get_object_prefix(user)}{file_name}'
        presigned_url = self._s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self._bucket_name, 'Key': key},
            ExpiresIn=expiration_in_seconds
        )
        return presigned_url
