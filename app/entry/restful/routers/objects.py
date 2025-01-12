from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse

from app.core.config.security.middlewares import get_current_user

router = APIRouter(
    prefix="/object",
    tags=["object"]
)


@router.post("")
def create_an_object(
        current_user: dict = Depends(get_current_user)
):
    return "OK"


@router.get("/redirect")
def root():
    return RedirectResponse(
        "https://aws.amazon.com/blogs/architecture/text-analytics-on-aws-implementing-a-data-lake-architecture-with"
        "-opensearch/")
