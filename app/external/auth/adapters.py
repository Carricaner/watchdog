from app.core.config.security.services import AuthServiceAdapter
from app.external.database.mongodb.managers import MongodbManager


class AuthServiceAdapterImpl(AuthServiceAdapter):
    def __init__(self, mongodb_manager: MongodbManager) -> None:
        self._mongodb_manager = mongodb_manager

    def get_user(self, username: str):
        # TODO
        return {
            "hashed_password": "$2b$12$r6IRtFLKBM06D5ozDx7uJOQgI2gvE88Y334yrOwcizzWfzPxYPdDm"
        }
