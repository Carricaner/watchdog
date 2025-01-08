from motor.motor_asyncio import AsyncIOMotorClient


class MongodbManager:
    def __init__(self, connection_url: str, env_str: str) -> None:
        self._db = AsyncIOMotorClient(connection_url)[env_str]

    def __get_collection(self, collection_name: str):
        return self._db[collection_name]

    def get_objects_collection(self):
        return self.__get_collection("objects")

    def get_access_links_collection(self):
        return self.__get_collection("accessLinks")


__all__ = [
    "MongodbManager"
]
