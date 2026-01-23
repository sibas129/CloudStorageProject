from aiogram import Bot
from aiogram.types import FSInputFile

from database.orm import Users, Folders, M2M_FoldersFolders, M2M_UsersFolders, M2M_FilesFolders, Files
from typing import List

from keyboards.personal import personal_ls_k


async def send_personal_ls_menu(
    current_folder_id: int,
    chat_id: int,
    message_id_to_delete: int,
    bot: Bot,
    database_worker,
    do_sort_alpha = None,
    do_sort_data = None,
) -> None:
    user: Users = await database_worker.custom_orm_select(
        cls_from=Users,
        where_params=[Users.telegram_id == chat_id],
        get_unpacked=True,
    )

    parent_folder = None
    root_folder_id = None

    if current_folder_id:
        target_folder: Folders = await database_worker.custom_orm_select(
            cls_from=Folders,
            where_params=[Folders.id == current_folder_id],
            get_unpacked=True,
        )
        parent_folder: M2M_FoldersFolders = await database_worker.custom_orm_select(
            cls_from=M2M_FoldersFolders,
            where_params=[M2M_FoldersFolders.child_folder_id == target_folder.id],
            get_unpacked=True,
        )

        if not parent_folder:
            fallback_string = "main_menu"
        else:
            fallback_string = (
                f"personal_ls|{parent_folder.parent_folder_id}"
            )
    else:
        root_folder_id: Folders = await database_worker.custom_orm_select(
            cls_from=M2M_UsersFolders.folder_id,
            where_params=[
                M2M_UsersFolders.user_id == user.id,
                M2M_UsersFolders.is_root == True,
            ],
            get_unpacked=True,
        )
        target_folder: Folders = await database_worker.custom_orm_select(
            cls_from=Folders,
            where_params=[Folders.id == root_folder_id],
            get_unpacked=True,
        )
        fallback_string = "main_menu"

    child_folders_ids: List[int] = await database_worker.custom_orm_select(
        cls_from=M2M_FoldersFolders.child_folder_id,
        where_params=[M2M_FoldersFolders.parent_folder_id == target_folder.id],
    )
    if do_sort_data:
        child_folders: List[Folders] = await database_worker.custom_orm_select(
            cls_from=Folders, where_params=[Folders.id.in_(child_folders_ids)], order_by=[Folders.created_at.desc()]
        )
    elif do_sort_alpha:
        child_folders: List[Folders] = await database_worker.custom_orm_select(
            cls_from=Folders, where_params=[Folders.id.in_(child_folders_ids)], order_by=[Folders.name.asc()]
        )
    else:
        child_folders: List[Folders] = await database_worker.custom_orm_select(
            cls_from=Folders, where_params=[Folders.id.in_(child_folders_ids)]
        )

    inner_files_ids: List[int] = await database_worker.custom_orm_select(
        cls_from=M2M_FilesFolders.file_id,
        where_params=[M2M_FilesFolders.folder_id == target_folder.id],
    )
    if do_sort_data:
        inner_files: List[Files] = await database_worker.custom_orm_select(
            cls_from=Files, where_params=[Files.id.in_(inner_files_ids)], order_by=[Files.created_at.desc()]
        )
    elif do_sort_alpha:
        inner_files: List[Files] = await database_worker.custom_orm_select(
            cls_from=Files, where_params=[Files.id.in_(inner_files_ids)], order_by=[Files.name.asc()]
        )
    else:
        inner_files: List[Files] = await database_worker.custom_orm_select(
            cls_from=Files, where_params=[Files.id.in_(inner_files_ids)]
        )

    markup_inline = personal_ls_k.get(
        folders=child_folders,
        files=inner_files,
        current_folder=target_folder,
        fallback_string=fallback_string,
        parent_folder_id=parent_folder.parent_folder_id if parent_folder and not parent_folder.parent_folder_id == root_folder_id else None,
    )

    photo = FSInputFile("src/personal.png")
    await bot.delete_message(chat_id=chat_id, message_id=message_id_to_delete)
    await bot.send_photo(
        chat_id=chat_id,
        photo=photo,
        caption=f"📂 {target_folder.name if current_folder_id and parent_folder else 'Личные файлы'}",
        reply_markup=markup_inline,
    )
