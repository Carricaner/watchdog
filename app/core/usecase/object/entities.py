from enum import Enum

from pydantic import BaseModel, ConfigDict, HttpUrl


class ObjectType(str, Enum):
    URL = "url"


class CreateAnObjectUseCaseInput(BaseModel):
    user_id: str
    type: ObjectType
    url: HttpUrl

    model_config = ConfigDict(use_enum_values=True)


if __name__ == "__main__":
    case_input = CreateAnObjectUseCaseInput(user_id="123", type=ObjectType.URL,
                                            url="https://aws.amazon.com/blogs/architecture/text-analytics-on-aws-implementing-a-data-lake-architecture-with-opensearch/")
    print(case_input.model_dump(mode="json"))
