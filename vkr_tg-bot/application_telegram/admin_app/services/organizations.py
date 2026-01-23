from admin_app.services.files import FileService
from admin_app.services.folders import FoldersService
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm import Organizations, M2M_UsersOrganizations, M2M_OrganizationsFolders, Users


class OrganizationService:
    def __init__(self, db_worker: DatabaseWorkerAsync):
        self.db_worker = db_worker
        self.file_service = FileService(db_worker)

    async def organization_by_id(self, org_id: int) -> dict | None:
        try:
            organization = await self.db_worker.custom_orm_select(
                cls_from=Organizations,
                where_params=[Organizations.id == org_id],
                get_unpacked=True
            )
            folders_tree, total_size = await self.file_service.build_tree_by_organization(org_id)
            user_list = await self.org_users(org_id)
            return {
                'id': organization.id,
                'user_id': organization.user_id,
                'name': organization.name,
                'is_deleted': organization.is_deleted,
                'created_at': organization.created_at,
                'users': user_list,
                'folder': folders_tree,
                'size': total_size,
            }

        except Exception as e:
            print(e)
            return {}

    async def org_users(self, org_id: int) -> list[dict]:
        org_users = await self.db_worker.custom_orm_select(
            M2M_UsersOrganizations,
            where_params=[M2M_UsersOrganizations.organization_id == org_id],
        )
        user_ids = [org_user.user_id for org_user in org_users]
        users_list = await self.db_worker.custom_orm_select(cls_from=Users, where_params=[Users.id.in_(user_ids)])
        return users_list

    async def delete_organization(self, org_id: int):
        root_orgfolder = await self.db_worker.custom_orm_select(
            cls_from=M2M_OrganizationsFolders,
            where_params=[
                M2M_OrganizationsFolders.organization_id == org_id,
                M2M_OrganizationsFolders.is_root == True,
            ],
            get_unpacked=True,
        )
        await self.db_worker.custom_delete_all(
            cls_from=Organizations,
            where_params=[Organizations.id == org_id],
        )
        await FoldersService(self.db_worker).recursive_delete_folders(root_orgfolder.folder_id)
        return
