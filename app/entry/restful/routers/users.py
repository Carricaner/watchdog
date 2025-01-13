from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config.di.containers import CoreContainer
from app.core.config.security.middlewares import get_current_user
from app.core.config.security.services import BcryptService
from app.core.domain.user.entities import User
from app.core.usecase.user.entities import SigninUseCaseInput
from app.core.usecase.user.usecases import AuthUseCase

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/signin")
@inject
async def sign_in(
        request_body: SigninUseCaseInput,
        hash_service: BcryptService = Depends(Provide[CoreContainer.hash_service]),
        auth_use_case: AuthUseCase = Depends(Provide[CoreContainer.auth_use_case])
):
    dict_dump = request_body.model_dump()
    dict_dump.update({"password": hash_service.hash(request_body.password)})
    await auth_use_case.sing_in(SigninUseCaseInput(**dict_dump))
    return "OK"


@router.post("/login")
@inject
async def login_in_for_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        auth_use_case: AuthUseCase = Depends(Provide[CoreContainer.auth_use_case])
):
    return await auth_use_case.log_in(form_data.username, form_data.password)


@router.get("/me")
async def me_user(
        current_user: User = Depends(get_current_user)
):
    return current_user
