from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.core.config.settings import GlobalSettings


class CoreContainer(DeclarativeContainer):
    # Config
    config = providers.Configuration(pydantic_settings=[GlobalSettings()])
