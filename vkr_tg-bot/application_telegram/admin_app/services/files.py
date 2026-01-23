from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm import M2M_UsersFolders, M2M_FilesFolders, M2M_FoldersFolders, Folders, Files, M2M_OrganizationsFolders


class FileService:
    def __init__(self, db_worker: DatabaseWorkerAsync):
        self.db_worker = db_worker

    async def build_tree_by_organization(self, org_id):
        root_orgfolder = await self.db_worker.custom_orm_select(
            cls_from=M2M_OrganizationsFolders,
            where_params=[
                M2M_OrganizationsFolders.organization_id == org_id,
                M2M_OrganizationsFolders.is_root == True,
            ],
            get_unpacked=True,
        )
        if root_orgfolder:
            folders_tree, total_size = await self.tree_by_folder_id(root_orgfolder.folder_id)
            return folders_tree, total_size
        return {}, 0

    async def build_tree_by_user(self, user_id: int) -> (dict, int):
        root_userfolder = await self.db_worker.custom_orm_select(
            cls_from=M2M_UsersFolders,
            where_params=[M2M_UsersFolders.user_id == user_id, M2M_UsersFolders.is_root == True],
            get_unpacked=True,
        )
        if root_userfolder:
            folders_tree, total_size = await self.tree_by_folder_id(root_userfolder.folder_id)
            return folders_tree, total_size
        return {}, 0

    async def get_files_by_folder_id(self, folder_id) -> (list, int):
        files = await self.db_worker.custom_orm_select(
            cls_from=M2M_FilesFolders,
            where_params=[M2M_FilesFolders.folder_id == folder_id],
        )
        file_ids = [file.id for file in files]
        files = await self.db_worker.custom_orm_select(
            cls_from=Files,
            where_params=[Files.id.in_(file_ids)],
        )
        list_files = []
        total_size = 0
        for file in files:
            list_files.append(
                {
                    'id': file.id,
                    'name': file.name,
                    'created_at': file.created_at,
                    'updated_at': file.updated_at,
                    'size': file.size,
                }
            )
            total_size += file.size
        return list_files, total_size

    async def tree_by_folder_id(self, folder_id):
        current_folder = await self.db_worker.custom_orm_select(
            cls_from=Folders,
            where_params=[Folders.id == folder_id],
            get_unpacked=True,
        )
        raw_folders = await self.db_worker.custom_orm_select(
            cls_from=M2M_FoldersFolders,
            where_params=[M2M_FoldersFolders.parent_folder_id == folder_id]
        )
        total_size = 0
        files, files_size = await self.get_files_by_folder_id(folder_id)
        folders = []
        total_size += files_size

        for raw_folder in raw_folders:
            folder, folders_size = await self.tree_by_folder_id(raw_folder.child_folder_id)
            folders.append(folder)
            total_size += folders_size

        structure = {
            'id': current_folder.id,
            'name': current_folder.name,
            'created_at': current_folder.created_at,
            'updated_at': current_folder.updated_at,
            'files': files,
            'folders': folders,
        }
        return structure, total_size
