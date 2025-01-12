from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.config.di.containers import CoreContainer
from app.core.usecase.user.usecases import AuthUseCase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/auth")


@inject
def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        auth_use_case: AuthUseCase = Depends(Provide[CoreContainer.auth_use_case])
):

    return auth_use_case.get_current_user(token)
