from pydantic import BaseModel


class AdminData(BaseModel):
    username: str
    password: str
