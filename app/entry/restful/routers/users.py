from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config.di.containers import CoreContainer
from app.core.config.security.middlewares import get_current_user
from app.core.usecase.user.inputs import SigninUseCaseInput
from app.core.usecase.user.usecases import AuthUseCase

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.post("/signin")
@inject
async def sign_in(
        request_body: SigninUseCaseInput,
        auth_use_case: AuthUseCase = Depends(Provide[CoreContainer.auth_use_case])
):
    response = await auth_use_case.sing_in(request_body)
    return "OK"


@router.post("/auth")
@inject
async def login_in_for_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        auth_use_case: AuthUseCase = Depends(Provide[CoreContainer.auth_use_case])
):
    return await auth_use_case.log_in(form_data.username, form_data.password)


@router.get("/me")
async def me_user(
        current_user: dict = Depends(get_current_user)
):
    return current_user
