from admin_app.services.files import FileService
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm import Users


class UserService:
    def __init__(self, db_worker: DatabaseWorkerAsync):
        self.db_worker = db_worker
        self.file_service = FileService(db_worker)

    async def user_by_id(self, user_id: int) -> dict | None:
        try:
            user = await self.db_worker.custom_orm_select(
                cls_from=Users,
                where_params=[Users.id == user_id],
                get_unpacked=True
            )
            folders_tree, total_size = await self.file_service.build_tree_by_user(user_id)
            return {
                'id': user.id,
                'telegram_id': user.telegram_id,
                'telegram_name': user.telegram_name,
                'created_at': user.created_at,
                'updated_at': user.updated_at,
                'folder': folders_tree,
                'size': total_size,
            }

        except Exception as e:
            print(e)
            return {}
