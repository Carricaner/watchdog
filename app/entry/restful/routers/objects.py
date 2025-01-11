from bson import ObjectId
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse

from app.core.config.di.containers import CoreContainer
from app.core.config.security.services import BcryptService
from app.external.database.mongodb.managers import MongodbManager
from app.external.database.mongodb.model.models import ObjectModel
from app.external.di.containers import ExternalContainer

router = APIRouter(
    prefix="/object",
    tags=["object"]
)


@router.get(
    "",
    response_model=ObjectModel
)
@inject
async def create_an_object_only_for_testing(
        mongodb_manager: MongodbManager = Depends(Provide[ExternalContainer.mongodb_manager])
):
    document_id = "677c4512428acdc6e7dbd299"
    query = {"_id": ObjectId(document_id)}
    document = await mongodb_manager.get_objects_collection().find_one(query)
    if document:
        return document
    return "NOT..OK.."


@router.get("/test-inject-service")
@inject
def test_inject_service(
        raw_str: str,
        hash_service: BcryptService = Depends(Provide[CoreContainer.hash_service])
):
    return hash_service.hash(raw_str)


@router.get("/redirect")
def root():
    return RedirectResponse(
        "https://aws.amazon.com/blogs/architecture/text-analytics-on-aws-implementing-a-data-lake-architecture-with"
        "-opensearch/")
