from aiogram import Bot

from database.orm.public_organizations_model import Organizations
from database.orm.public_folders_model import Folders
from database.orm.public_files_model import Files
from database.orm.public_m2m_organizations_folders_model import M2M_OrganizationsFolders
from database.orm.public_m2m_folders_folders_model import M2M_FoldersFolders
from database.orm.public_m2m_files_folders_model import M2M_FilesFolders

from keyboards.organizations import organizations_ls_k

from typing import List

async def send_organization_ls_menu(
    chat_id: int,
    message_id_to_delete: int,
    current_folder_id: int,
    current_organization_id: int,
    bot: Bot,
    database_worker,
    do_sort_alpha=None,
    do_sort_data=None,
) -> None:
    current_organization: Organizations = await database_worker.custom_orm_select(
        cls_from=Organizations,
        where_params=[Organizations.id == current_organization_id],
        get_unpacked=True,
    )

    if current_folder_id:
        current_folder: Folders = await database_worker.custom_orm_select(
            cls_from=Folders,
            where_params=[Folders.id == current_folder_id],
            get_unpacked=True,
        )

        parent_folder: Folders = await database_worker.custom_orm_select(
            cls_from=M2M_FoldersFolders,
            where_params=[M2M_FoldersFolders.child_folder_id == current_folder.id],
            get_unpacked=True,
        )

        if not parent_folder:
            fallback_string = f"organization_menu|{current_organization_id}"
        else:
            fallback_string = (
                f"organizations_ls|{parent_folder.parent_folder_id}|{current_organization_id}"
            )
    else:
        root_folder_id: Folders = await database_worker.custom_orm_select(
            cls_from=M2M_OrganizationsFolders.folder_id,
            where_params=[
                M2M_OrganizationsFolders.organization_id == current_organization_id,
                M2M_OrganizationsFolders.is_root == True,
            ],
            get_unpacked=True,
        )
        current_folder: Folders = await database_worker.custom_orm_select(
            cls_from=Folders,
            where_params=[Folders.id == root_folder_id],
            get_unpacked=True,
        )
        fallback_string = f"organization_menu|{current_organization_id}"

    child_folders_ids: List[int] = await database_worker.custom_orm_select(
        cls_from=M2M_FoldersFolders.child_folder_id,
        where_params=[M2M_FoldersFolders.parent_folder_id == current_folder.id],
    )

    if do_sort_alpha:
        child_folders: List[Folders] = await database_worker.custom_orm_select(
            cls_from=Folders, where_params=[Folders.id.in_(child_folders_ids)], order_by=[Folders.name.asc()]
        )
    elif do_sort_data:
        child_folders: List[Folders] = await database_worker.custom_orm_select(
            cls_from=Folders, where_params=[Folders.id.in_(child_folders_ids)], order_by=[Folders.created_at.desc()]
        )
    else:
        child_folders: List[Folders] = await database_worker.custom_orm_select(
            cls_from=Folders, where_params=[Folders.id.in_(child_folders_ids)]
        )

    inner_files_ids: List[int] = await database_worker.custom_orm_select(
        cls_from=M2M_FilesFolders.file_id,
        where_params=[M2M_FilesFolders.folder_id == current_folder.id],
    )
    if do_sort_alpha:
        inner_files: List[Files] = await database_worker.custom_orm_select(
            cls_from=Files, where_params=[Files.id.in_(inner_files_ids)], order_by=[Files.name.asc()]
        )
    elif do_sort_data:
        inner_files: List[Files] = await database_worker.custom_orm_select(
            cls_from=Files, where_params=[Files.id.in_(inner_files_ids)], order_by=[Files.created_at.desc()]
        )
    else:
        inner_files: List[Files] = await database_worker.custom_orm_select(
            cls_from=Files, where_params=[Files.id.in_(inner_files_ids)]
        )

    markup_inline = organizations_ls_k.get(
        folders=child_folders,
        files=inner_files,
        current_folder=current_folder,
        fallback_string=fallback_string,
        organization_id=current_organization_id,
    )

    await bot.delete_message(chat_id=chat_id, message_id=message_id_to_delete)
    await bot.send_message(
        chat_id=chat_id,
        text=f"🏣 {current_organization.name} | {current_folder.name if current_folder_id and parent_folder else 'Файлы организации'}",
        reply_markup=markup_inline,
    )