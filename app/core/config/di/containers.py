from datetime import timedelta

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.core.config.security.services import BcryptService, JWTService, JWTAlgorithm, AuthService, AuthServiceAdapter
from app.core.config.settings import GlobalSettings
from app.core.usecase.user.adapters import UserUseCaseAdapter
from app.core.usecase.user.usecases import AuthUseCase


class CoreContainer(DeclarativeContainer):
    # Config
    config = providers.Configuration(pydantic_settings=[GlobalSettings()])

    # Security
    hash_service = providers.Singleton(BcryptService)
    jwt_service = providers.Singleton(JWTService,
                                      secret_key=config.authentication.secret_key,
                                      algorithm=JWTAlgorithm.HS256,
                                      token_lifetime=timedelta(minutes=1440))
    auth_service_adapter = providers.AbstractSingleton(AuthServiceAdapter)
    auth_service = providers.Singleton(AuthService, auth_service_adapter=auth_service_adapter,
                                       hash_service=hash_service)

    # Use cases
    user_use_case_adapter = providers.AbstractSingleton(UserUseCaseAdapter)
    auth_use_case = providers.Singleton(AuthUseCase, auth_service=auth_service, jwt_service=jwt_service,
                                        user_use_case_adapter=user_use_case_adapter)
