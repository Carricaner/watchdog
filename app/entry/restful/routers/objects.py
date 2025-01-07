from typing import Annotated, Optional

from bson import ObjectId
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BeforeValidator, BaseModel, Field, HttpUrl, ConfigDict
from starlette.responses import RedirectResponse

from app.core.config.settings import GlobalSettings
from app.core.di.containers import CoreContainer

router = APIRouter(
    prefix="/object",
    tags=["object"]
)

MongodbObjectId = Annotated[str, BeforeValidator(str)]


class ObjectModel(BaseModel):
    id: Optional[MongodbObjectId] = Field(alias="_id", default=None)
    type: str = Field(...)
    url: HttpUrl = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


@router.get(
    "",
    response_model=ObjectModel
)
@inject
async def create_an_object_only_for_testing(
    global_settings: GlobalSettings = Depends(Provide[CoreContainer.global_settings])
):
    connection_url = global_settings.mongodb.connection_url
    client = AsyncIOMotorClient(connection_url)
    db = client["dev"]
    collection = db["objects"]

    document_id = "677c4512428acdc6e7dbd299"
    query = {"_id": ObjectId(document_id)}
    document = await collection.find_one(query)
    if document:
        return document
    return "NOT..OK.."



@router.get("/redirect")
def root():
    return RedirectResponse(
        "https://aws.amazon.com/blogs/architecture/text-analytics-on-aws-implementing-a-data-lake-architecture-with"
        "-opensearch/")
