from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.core.config.di.containers import CoreContainer
from app.external.database.mongodb.managers import MongodbManager


class ExternalContainer(DeclarativeContainer):
    core_container = providers.Container(CoreContainer)

    # MongoDB Manager
    mongodb_manager = providers.Singleton(
        MongodbManager,
        connection_url=core_container.global_settings().mongodb.connection_url,
        env_str=core_container.global_settings().server_mode
    )


