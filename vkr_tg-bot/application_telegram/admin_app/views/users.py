from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette import status

from admin_app.schemas.auth import TokenData
from admin_app.schemas.users import UserResponse, UserWithFolders
from admin_app.services.admins import get_current_user
from admin_app.services.users import UserService
from config import database_engine_async
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm import Users

user_router = APIRouter()
database_worker = DatabaseWorkerAsync(database_engine_async)


@user_router.get('/users')
async def get_users(current_user: Annotated[TokenData, Depends(get_current_user)]) -> list[UserResponse]:
    users_list = await database_worker.custom_orm_select(cls_from=Users)
    return users_list


@user_router.get('/users/{user_id}', response_model=UserWithFolders)
async def get_user(user_id: int, current_user: Annotated[TokenData, Depends(get_current_user)]):
    user = await UserService(database_worker).user_by_id(user_id)
    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={'message': 'User files does not exist'})
    return user
