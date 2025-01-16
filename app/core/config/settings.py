import os
from enum import Enum

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerEnvironment(Enum):
    LOCAL = "local"
    DEVELOP = "dev"
    PRODUCTION = "prod"

    @staticmethod
    def from_str(env_string: str):
        return ServerEnvironment(env_string.lower())


class AuthenticationSettings(BaseModel):
    secret_key: str
    algorithm: str = Field(default="HS256")
    expiration_period: int = Field(default=3600)


class MongodbSettings(BaseModel):
    connection_url: str
    database: str


class AWSSettings(BaseModel):
    access_key: str
    secret_key: str
    region: str


class GlobalSettings(BaseSettings):
    server_mode: str
    authentication: AuthenticationSettings
    mongodb: MongodbSettings
    aws: AWSSettings

    model_config = SettingsConfigDict(
        env_file=f'env/{ServerEnvironment.from_str(os.environ.get("WATCHDOG_ENV")).value}/.env',
        env_nested_delimiter="__",
        extra="ignore"

    )


__all__ = [
    "GlobalSettings",
    "ServerEnvironment"
]
