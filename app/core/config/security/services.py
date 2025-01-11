from abc import ABC, abstractmethod
from datetime import timedelta, datetime, timezone
from enum import Enum

import jwt
from jwt import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel


class JWTAlgorithm(Enum):
    HS256 = "HS256"
    HS384 = "HS384"
    HS512 = "HS512"
    RS256 = "RS256"
    RS384 = "RS384"
    RS512 = "RS512"
    ES256 = "ES256"
    ES384 = "ES384"
    ES512 = "ES512"
    PS256 = "PS256"
    PS384 = "PS384"
    PS512 = "PS512"


class BcryptService:

    def __init__(self) -> None:
        self._context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, input_str: str):
        return self._context.hash(input_str)

    def verify(self, unhashed: str, hashed: str) -> bool:
        return self._context.verify(unhashed, hashed)


class JWTDecodeResponse(BaseModel):
    success: bool = False
    payload: dict = None
    message: str = ""


class JWTService:
    def __init__(self, secret_key: str,
                 algorithm: JWTAlgorithm = JWTAlgorithm.HS256,
                 token_lifetime: timedelta = timedelta(minutes=1440)) -> None:
        self._secret_key = secret_key
        self._algorithm: JWTAlgorithm = algorithm
        self._token_lifetime: timedelta = token_lifetime

    def encode(self, data: dict, token_lifetime: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (token_lifetime or self._token_lifetime)
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode,
            self._secret_key,
            algorithm=self._algorithm.value
        )

    def decode(self, token: str) -> JWTDecodeResponse:
        try:
            return JWTDecodeResponse(
                success=True,
                payload=jwt.decode(token, self._secret_key, algorithms=[self._algorithm.value])
            )
        except InvalidTokenError:
            return JWTDecodeResponse()


class AuthServiceAdapter(ABC):
    @abstractmethod
    async def get_user(self, username: str):
        pass


class AuthService:
    def __init__(self, auth_service_adapter: AuthServiceAdapter,
                 hash_service: BcryptService) -> None:
        self._auth_service_adapter = auth_service_adapter
        self._hash_service = hash_service

    async def authenticate_user(self, username: str, password: str) -> bool:
        user = await self._auth_service_adapter.get_user(username)
        return user is not None and self._hash_service.verify(password, user.hashed_password)
