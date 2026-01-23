from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm import M2M_FilesFolders, Folders, Files, M2M_FoldersFolders, M2M_UsersFolders, \
    M2M_OrganizationsFolders


class FoldersService:
    def __init__(self, database_worker: DatabaseWorkerAsync):
        self.database_worker = database_worker

    async def check_is_root(self, folder_id: int) -> bool:
        user_folder = None
        organization_folder = None
        try:
            user_folder = await self.database_worker.custom_orm_select(
                cls_from=M2M_UsersFolders,
                where_params=[M2M_UsersFolders.folder_id == folder_id],
                get_unpacked=True,
            )

            organization_folder = await self.database_worker.custom_orm_select(
                cls_from=M2M_OrganizationsFolders,
                where_params=[M2M_OrganizationsFolders.folder_id == folder_id],
                get_unpacked=True,
            )
        except Exception as e:
            pass

        if user_folder and user_folder.is_root:
            return True
        if organization_folder and organization_folder.is_root:
            return True

        return False

    async def recursive_delete_folders(self, folder_id):
        await self.delete_files(folder_id)

        await self.database_worker.custom_delete_all(
            cls_from=Folders,
            where_params=[Folders.id == folder_id]
        )
        await self.delete_child_folders(folder_id)
        return {}

    async def delete_child_folders(self, folder_id):
        m2m_folders = await self.database_worker.custom_orm_select(
            cls_from=M2M_FoldersFolders,
            where_params=[M2M_FoldersFolders.parent_folder_id == folder_id]
        )
        for m2m_folder in m2m_folders:
            await self.delete_files(m2m_folder.child_folder_id)
            await self.delete_child_folders(m2m_folder.child_folder_id)
            await self.database_worker.custom_delete_all(
                cls_from=Folders,
                where_params=[Folders.id == m2m_folder.child_folder_id]
            )

    async def delete_files(self, folder_id):
        m2m_files = await self.database_worker.custom_orm_select(
            cls_from=M2M_FilesFolders,
            where_params=[Folders.id == folder_id],
        )
        files_ids = [_.file_id for _ in m2m_files]

        await self.database_worker.custom_delete_all(
            cls_from=Files,
            where_params=[Folders.id.in_(files_ids)],
        )
