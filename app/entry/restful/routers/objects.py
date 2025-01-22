from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, File, UploadFile

from app.core.config.di.containers import CoreContainer
from app.core.config.security.middlewares import get_current_user
from app.core.domain.user.entities import User
from app.core.usecase.object.usecases import ObjectUseCase

router = APIRouter(
    prefix="/object",
    tags=["object"]
)


@router.post("/file")
@inject
async def create_an_file(
        file: UploadFile = File(...),
        current_user: User = Depends(get_current_user),
        object_use_case: ObjectUseCase = Depends(Provide[CoreContainer.object_use_case])
):
    await object_use_case.create_a_file(current_user, file)
    return "OK"


@router.get("/file/all")
@inject
async def get_all_file_names(
        current_user: User = Depends(get_current_user),
        object_use_case: ObjectUseCase = Depends(Provide[CoreContainer.object_use_case])
):
    return await object_use_case.get_all_user_files(current_user)
