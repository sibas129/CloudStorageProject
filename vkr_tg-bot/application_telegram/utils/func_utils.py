from aiogram.types import Message

import io
import base64
from PIL import Image
import xml.etree.ElementTree as ET
import uuid

from config import database_engine_async

from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_users_model import Users
from database.orm.public_folders_model import Folders
from database.orm.public_m2m_users_folders_model import M2M_UsersFolders

database_worker = DatabaseWorkerAsync(database_engine_async)


async def auto_registration(message: Message) -> None:
    user: Users = await database_worker.custom_orm_select(
        cls_from=Users,
        where_params=[Users.telegram_id == message.chat.id],
        get_unpacked=True,
    )

    if not user:
        data_to_insert = {
            "telegram_id": message.chat.id,
            "telegram_name": message.chat.username,
        }
        await database_worker.custom_insert(cls_to=Users, data=[data_to_insert])
        user: Users = await database_worker.custom_orm_select(
            cls_from=Users,
            where_params=[Users.telegram_id == message.chat.id],
            get_unpacked=True,
        )

        folder_name = str(uuid.uuid4())
        data_to_insert = {"name": folder_name}
        await database_worker.custom_insert(cls_to=Folders, data=[data_to_insert])
        root_folder: Folders = await database_worker.custom_orm_select(
            cls_from=Folders,
            where_params=[Folders.name == folder_name],
            get_unpacked=True,
        )

        data_to_insert = {
            "user_id": user.id,
            "folder_id": root_folder.id,
            "is_root": True,
        }
        await database_worker.custom_insert(
            cls_to=M2M_UsersFolders, data=[data_to_insert]
        )
