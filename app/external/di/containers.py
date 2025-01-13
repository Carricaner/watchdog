from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.core.config.settings import GlobalSettings
from app.external.database.mongodb.managers import MongodbManager
from app.external.object.adapters import ObjectUseCaseAdapterImpl
from app.external.user.adapters import UserUseCaseAdapterImpl


class ExternalContainer(DeclarativeContainer):
    # Config
    config = providers.Configuration(pydantic_settings=[GlobalSettings()])

    # MongoDB Manager
    mongodb_manager = providers.Singleton(
        MongodbManager,
        connection_url=config.mongodb.connection_url,
        env_str=config.server_mode
    )

    # Adapters
    user_use_case_adapter = providers.Singleton(UserUseCaseAdapterImpl, mongodb_manager=mongodb_manager)
    object_use_case_adapter = providers.Singleton(ObjectUseCaseAdapterImpl, mongodb_manager=mongodb_manager)
