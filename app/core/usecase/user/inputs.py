from pydantic import BaseModel


class SigninUseCaseInput(BaseModel):
    username: str
    email: str
    password: str
