from datetime import datetime, timedelta, timezone
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from typing import Annotated

from admin_app.schemas.auth import TokenData, AdminModel
from admin_app.schemas.admins import AdminData
from database.oop.database_worker_async import DatabaseWorkerAsync
from config import database_engine_async
from database.orm import Admins

database_worker = DatabaseWorkerAsync(database_engine_async)

SECRET_KEY = "da5e2c8acedfcfbea714634ab5a316a6e151d9769b063dfa9f08d8bf39203c9f"  # to env!
ALGORITHM = "HS256"  # to env!
ACCESS_TOKEN_EXPIRE_MINUTES = 15

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class AdminService:
    def __init__(self, db_worker: DatabaseWorkerAsync):
        self.db_worker = db_worker

    async def add_admin(self, admin_data: AdminData) -> bool:
        if not admin_data.password:
            return False
        check_admin = await self.db_worker.custom_orm_select(
            cls_from=Admins,
            where_params=[Admins.username == admin_data.username],
            get_unpacked=True
        )
        if check_admin:
            return False

        a = Admins(username=admin_data.username, is_superadmin=False)
        a.set_password(admin_data.password)
        admin = [columns_to_dict(a)]
        await self.db_worker.custom_insert(
            cls_to=Admins,
            data=admin
        )

        check_admin = await self.db_worker.custom_orm_select(
            cls_from=Admins,
            where_params=[Admins.username == admin_data.username],
            get_unpacked=True
        )
        if check_admin:
            return True
        return False

    async def get_admin_list(self):
        admins_list = await self.db_worker.custom_orm_select(
            cls_from=[Admins.id, Admins.username, Admins.is_superadmin]
        )
        result_list = [AdminModel(id=admin.id,
                                  username=admin.username,
                                  is_superadmin=admin.is_superadmin) for admin in admins_list]
        return result_list

    async def remove_admin(self, admin_id: int) -> bool:
        admin = await self.db_worker.custom_orm_select(
            cls_from=Admins,
            where_params=[Admins.id == admin_id],
            get_unpacked=True
        )
        if admin:
            if admin.is_superadmin:
                return False
            await self.db_worker.custom_delete_all(
                cls_from=Admins,
                where_params=[Admins.id == admin_id]
            )
        return True


def columns_to_dict(self):
    dict_ = {}
    for key in self.__mapper__.c.keys():
        if key != "id":
            dict_[key] = getattr(self, key)
    return dict_


async def get_admin(username: str):
    admin = await database_worker.custom_orm_select(
        cls_from=Admins,
        where_params=[Admins.username == username],
        get_unpacked=True
    )
    return admin


async def authenticate_admin(username: str, password: str) -> dict | bool:
    admin = await get_admin(username)
    if not admin:
        return False
    if not admin.check_password(password):
        return False
    return columns_to_dict(admin)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        is_superadmin: bool = payload.get("isa")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, is_superadmin=is_superadmin)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_admin(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_user_superadmin(current_user: Annotated[AdminModel, Depends(get_current_user)]):
    if not current_user.is_superadmin:
        raise HTTPException(status_code=400, detail="Not superadmin")
    return current_user