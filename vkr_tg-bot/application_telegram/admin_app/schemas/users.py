from datetime import datetime

from pydantic import BaseModel, field_validator

from admin_app.schemas.files import FolderResponse
from admin_app.schemas.validators import format_size


class UserResponse(BaseModel):
    id: int
    telegram_id: int
    telegram_name: str
    created_at: datetime
    updated_at: datetime


class UserWithFolders(UserResponse):
    size: int
    folder: FolderResponse

    @field_validator('size')
    def format_size_validator(cls, value):
        if isinstance(value, int):
            return format_size(value)
        raise ValueError('size must be an integer')
