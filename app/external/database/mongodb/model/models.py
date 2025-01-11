from typing import Annotated, Optional

from pydantic import BeforeValidator, BaseModel, Field, HttpUrl, ConfigDict

MongodbObjectId = Annotated[str, BeforeValidator(str)]


class BasicMongoDbModel(BaseModel):
    id: Optional[MongodbObjectId] = Field(alias="_id", default=None)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )


class UserModel(BasicMongoDbModel):
    username: str = Field(...)
    hashed_password: str = Field(...)


class ObjectModel(BasicMongoDbModel):
    id: Optional[MongodbObjectId] = Field(alias="_id", default=None)
    type: str = Field(...)
    url: HttpUrl = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
