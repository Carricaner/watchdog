from typing import Annotated, Optional

from bson import ObjectId
from fastapi import APIRouter
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BeforeValidator, BaseModel, Field, HttpUrl, ConfigDict
from starlette.responses import RedirectResponse

from app.core.config.settings import global_settings

router = APIRouter(
    prefix="/object",
    tags=["object"]
)

connection_url = "mongodb+srv://macbookm2pro:kA6g2fCtmlB3AH4e@cluster0.aoizo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = AsyncIOMotorClient(connection_url)
db = client["dev"]
collection = db["objects"]

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
async def create_an_object():
    document_id = "677c4512428acdc6e7dbd299"
    query = {"_id": ObjectId(document_id)}
    document = await collection.find_one(query)
    if document:
        return document
    return "NOT..OK.."


@router.get("/settings")
def get_settings():
    return global_settings


@router.get("/redirect")
def root():
    return RedirectResponse(
        "https://aws.amazon.com/blogs/architecture/text-analytics-on-aws-implementing-a-data-lake-architecture-with"
        "-opensearch/")
