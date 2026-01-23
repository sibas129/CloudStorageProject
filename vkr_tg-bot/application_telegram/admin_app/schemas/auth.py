from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    is_superadmin: bool | None = None


class AdminModel(BaseModel):
    id: int
    username: str
    is_superadmin: bool
