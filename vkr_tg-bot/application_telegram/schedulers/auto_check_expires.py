from typing import List
from datetime import datetime

from config import database_engine_async

from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_m2m_users_folders_model import M2M_UsersFolders


database_worker = DatabaseWorkerAsync(database_engine_async)


async def auto_check_expires() -> None:
    current_date = datetime.now()
    target_ids: List[int] = await database_worker.custom_orm_select(
        cls_from=M2M_UsersFolders.id,
        where_params=[
            M2M_UsersFolders.is_owner == False,
            M2M_UsersFolders.is_root == False,
            M2M_UsersFolders.expired_at > current_date,
        ],
    )
    await database_worker.custom_delete_all(
        cls_from=M2M_UsersFolders, where_params=[M2M_UsersFolders.id.in_(target_ids)]
    )
