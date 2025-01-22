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

    async def upload_file(self, user: User, file: UploadFile):
        file_content = await file.read()
        self._s3_client.put_object(
            Bucket=self._bucket_name,
            Key=f"user/{user.id}/{file.filename}",
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
