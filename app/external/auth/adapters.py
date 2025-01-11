from app.core.config.security.services import AuthServiceAdapter
from app.external.database.mongodb.managers import MongodbManager
from app.external.database.mongodb.model.models import UserModel


class AuthServiceAdapterImpl(AuthServiceAdapter):
    def __init__(self, mongodb_manager: MongodbManager) -> None:
        self._mongodb_manager = mongodb_manager

    async def get_user(self, username: str):
        query = {"username": username}
        document = await self._mongodb_manager.get_users_collection().find_one(query)
        if not document:
            return None
        return UserModel(**document)
