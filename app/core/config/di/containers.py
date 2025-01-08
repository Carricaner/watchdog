from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.core.config.settings import GlobalSettings


class CoreContainer(DeclarativeContainer):
    # Global Settings
    global_settings = providers.Singleton(GlobalSettings)
