from app.core.domain.user.entities import User
from app.core.usecase.user.adapters import UserUseCaseAdapter
from app.core.usecase.user.inputs import SigninUseCaseInput
from app.external.database.mongodb.managers import MongodbManager


class UserUseCaseAdapterImpl(UserUseCaseAdapter):

    def __init__(self, mongodb_manager: MongodbManager) -> None:
        self._mongodb_manager = mongodb_manager

    async def get_user_by_email(self, email: str) -> User:
        query = {"email": email}
        document = await self._mongodb_manager.get_users_collection().find_one(query)
        return User(**document)

    async def create_user(self, sign_in_input: SigninUseCaseInput):
        dump = sign_in_input.model_dump()
        dump["disabled"] = False
        result = await self._mongodb_manager.get_users_collection().insert_one(dump)
        return True
