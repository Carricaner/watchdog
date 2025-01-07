import os
from enum import Enum

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerEnvironment(Enum):
    LOCAL = "local"
    DEVELOP = "dev"
    PRODUCTION = "prod"

    @staticmethod
    def from_str(env_string: str):
        return ServerEnvironment(env_string.lower())


class MongodbSettings(BaseModel):
    connection_url: str
    database: str


class GlobalSettings(BaseSettings):
    server_mode: str
    mongodb: MongodbSettings

    model_config = SettingsConfigDict(
        env_file=f'env/{ServerEnvironment.from_str(os.environ.get("WATCHDOG_ENV")).value}/.env',
        env_nested_delimiter="__",
        extra="ignore"

    )


global_settings = GlobalSettings()

__all__ = [
    "global_settings",
    "ServerEnvironment"
]
