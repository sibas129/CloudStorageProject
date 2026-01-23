from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, field_validator

from admin_app.schemas.validators import format_size


class FileResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    size: int | None

    @field_validator('size')
    def format_size_validator(cls, value):
        if isinstance(value, int):
            return format_size(value)
        raise ValueError('size must be an integer')


class FolderResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    files: List[Optional[FileResponse]]
    folders: List[Optional['FolderResponse']]
