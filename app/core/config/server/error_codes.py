from enum import Enum


class ErrorCode(Enum):
    ENTITY_INVALIDATION = 1001
    GENERAL_HTTP = 2001


__all__ = [
    "ErrorCode",
]
