from pydantic import BaseModel, Field, AliasChoices


class User(BaseModel):
    id: str = Field(default=None, alias="user_id", validation_alias=AliasChoices("id", "user_id"))
    username: str
    email: str | None = None
    disabled: bool | None = None
    password: str | None = None


if __name__ == "__main__":
    dict = {
        "user_id": "123",
        "username": "twen"
    }
    print(User(**dict).model_dump(by_alias=True))
