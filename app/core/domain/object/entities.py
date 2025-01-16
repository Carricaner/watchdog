from enum import Enum


class ObjectType(str, Enum):
    URL = "url"
    FILE = "file"