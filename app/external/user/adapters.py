from app.core.usecase.user.adapters import UserUseCaseAdapter
from app.core.usecase.user.inputs import SigninUseCaseInput
from app.external.database.mongodb.managers import MongodbManager


class UserUseCaseAdapterImpl(UserUseCaseAdapter):

    def __init__(self, mongodb_manager: MongodbManager) -> None:
        self._mongodb_manager = mongodb_manager

    async def get_user_by_email(self, email: str):
        query = {"email": email}
        document = await self._mongodb_manager.get_users_collection().find_one(query)

    async def create_user(self, sign_in_input: SigninUseCaseInput):
        dump = sign_in_input.model_dump()
        dump["disable"] = False
        result = await self._mongodb_manager.get_objects_collection().insert_one(dump)
        return True
