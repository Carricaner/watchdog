from app.core.domain.user.entities import User
from app.core.usecase.object.adapters import ObjectUseCaseAdapter
from app.core.usecase.object.entities import CreateAnObjectUseCaseInput
from app.external.database.mongodb.managers import MongodbManager


class ObjectUseCaseAdapterImpl(ObjectUseCaseAdapter):

    def __init__(self, mongodb_manager: MongodbManager) -> None:
        self._mongodb_manager = mongodb_manager

    async def create_an_object(self, user: User, body: CreateAnObjectUseCaseInput):
        model_dump = body.model_dump(mode="json")
        model_dump["user_id"] = user.id
        result = await self._mongodb_manager.get_objects_collection().insert_one(model_dump)
        return result
