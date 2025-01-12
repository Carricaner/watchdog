from pydantic import BaseModel


class LoginUseCaseOutput(BaseModel):
    success: bool = False
    token: str = ""
