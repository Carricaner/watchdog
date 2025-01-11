from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.core.config.settings import GlobalSettings
from app.external.auth.adapters import AuthServiceAdapterImpl
from app.external.database.mongodb.managers import MongodbManager


class ExternalContainer(DeclarativeContainer):
    # Config
    config = providers.Configuration(pydantic_settings=[GlobalSettings()])

    # MongoDB Manager
    mongodb_manager = providers.Singleton(
        MongodbManager,
        connection_url=config.mongodb.connection_url,
        env_str=config.server_mode
    )

    # Auth
    auth_service_adapter = providers.Singleton(AuthServiceAdapterImpl, mongodb_manager=mongodb_manager)
