from typing import Annotated, Optional

from pydantic import BeforeValidator, BaseModel, Field, HttpUrl, ConfigDict

MongodbObjectId = Annotated[str, BeforeValidator(str)]


class ObjectModel(BaseModel):
    id: Optional[MongodbObjectId] = Field(alias="_id", default=None)
    type: str = Field(...)
    url: HttpUrl = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
