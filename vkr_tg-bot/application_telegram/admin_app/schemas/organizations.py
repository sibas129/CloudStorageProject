from datetime import datetime

from pydantic import BaseModel, field_validator
from typing import List

from admin_app.schemas.files import FolderResponse
from admin_app.schemas.users import UserResponse
from admin_app.schemas.validators import format_size


class OrganizationResponse(BaseModel):
    id: int
    user_id: int
    name: str
    is_deleted: bool
    created_at: datetime


class OrganizationsWithFolders(OrganizationResponse):
    users: List[UserResponse]
    size: int
    folder: FolderResponse

    @field_validator('size')
    def format_size_validator(cls, value):
        if isinstance(value, int):
            return format_size(value)
        raise ValueError('size must be an integer')
