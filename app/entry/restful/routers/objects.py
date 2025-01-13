from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse

from app.core.config.di.containers import CoreContainer
from app.core.config.security.middlewares import get_current_user
from app.core.domain.user.entities import User
from app.core.usecase.object.entities import CreateAnObjectUseCaseInput
from app.core.usecase.object.usecases import ObjectUseCase

router = APIRouter(
    prefix="/object",
    tags=["object"]
)


@router.post("")
@inject
async def create_an_object(
        request_body: CreateAnObjectUseCaseInput,
        current_user: User = Depends(get_current_user),
        object_use_case: ObjectUseCase = Depends(Provide[CoreContainer.object_use_case])
):
    await object_use_case.create_an_object(current_user, request_body)
    return "OK"


@router.get("/redirect")
def root():
    return RedirectResponse(
        "https://aws.amazon.com/blogs/architecture/text-analytics-on-aws-implementing-a-data-lake-architecture-with"
        "-opensearch/")
