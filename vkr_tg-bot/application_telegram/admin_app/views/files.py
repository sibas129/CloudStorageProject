from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse
from typing import Annotated

from admin_app.schemas.auth import TokenData
from admin_app.services.admins import get_current_user
from admin_app.services.folders import FoldersService
from config import database_engine_async
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm import Files
from utils.s3.s3_worker import S3Worker

files_router = APIRouter()
database_worker = DatabaseWorkerAsync(database_engine_async)
s3_worker = S3Worker()


@files_router.delete("/files/{file_id}")
async def delete_file(file_id: int, current_user: Annotated[TokenData, Depends(get_current_user)]):
    file = await database_worker.custom_orm_select(
        cls_from=Files,
        where_params=[Files.id == file_id],
        get_unpacked=True,
    )

    s3_worker.delete_file(path=file.path)
    await database_worker.custom_delete_all(
        cls_from=Files,
        where_params=[Files.id == file_id]
    )

    return {}


@files_router.delete("/folders/{folder_id}")
async def delete_folders(folder_id: int, current_user: Annotated[TokenData, Depends(get_current_user)]):
    service = FoldersService(database_worker)
    folder_is_root = await service.check_is_root(folder_id)

    if folder_is_root:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'error': 'root directory cannot be deleted'},
        )
    await service.recursive_delete_folders(folder_id)
    return {}
