from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.enums.parse_mode import ParseMode

from typing import List

from config import database_engine_async

from keyboards.shared import shared_ls_k, shared_file_menu_k

from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_users_model import Users
from database.orm.public_m2m_users_folders_model import M2M_UsersFolders
from database.orm.public_m2m_folders_folders_model import M2M_FoldersFolders
from database.orm.public_m2m_files_folders_model import M2M_FilesFolders
from database.orm.public_files_model import Files
from database.orm.public_folders_model import Folders


router = Router()
database_worker = DatabaseWorkerAsync(database_engine_async)


@router.callback_query(F.data.startswith("shared_ls"))
async def shared_ls(callback: CallbackQuery) -> None:
    current_folder_id: int = int(callback.data.split("|")[1])

    user: Users = await database_worker.custom_orm_select(
        cls_from=Users,
        where_params=[Users.telegram_id == callback.message.chat.id],
        get_unpacked=True,
    )

    inner_files: List[Files] = []

    if current_folder_id:
        current_folder: Folders = await database_worker.custom_orm_select(
            cls_from=Folders,
            where_params=[Folders.id == current_folder_id],
            get_unpacked=True,
        )
        current_folder_for_user: M2M_UsersFolders = (
            await database_worker.custom_orm_select(
                cls_from=M2M_UsersFolders,
                where_params=[
                    M2M_UsersFolders.folder_id == current_folder.id,
                    M2M_UsersFolders.expired_at != None,
                    M2M_UsersFolders.user_id == user.id,
                ],
            )
        )

        inner_folders_ids: List[int] = await database_worker.custom_orm_select(
            cls_from=M2M_FoldersFolders.child_folder_id,
            where_params=[M2M_FoldersFolders.parent_folder_id == current_folder.id],
        )
        inner_folders: List[Folders] = await database_worker.custom_orm_select(
            cls_from=Folders, where_params=[Folders.id.in_(inner_folders_ids)]
        )

        inner_files_ids: List[int] = await database_worker.custom_orm_select(
            cls_from=M2M_FilesFolders.file_id,
            where_params=[M2M_FilesFolders.folder_id == current_folder.id],
        )
        inner_files: List[Files] = await database_worker.custom_orm_select(
            cls_from=Files, where_params=[Files.id.in_(inner_files_ids)]
        )

        if current_folder_for_user:
            fallback_string = f"shared_ls|0"
        else:
            parent_folder: M2M_FoldersFolders = await database_worker.custom_orm_select(
                cls_from=M2M_FoldersFolders,
                where_params=[M2M_FoldersFolders.child_folder_id == current_folder.id],
                get_unpacked=True,
            )
            fallback_string = f"shared_ls|{parent_folder.parent_folder_id}"
    else:
        shared_folders_ids: List[int] = await database_worker.custom_orm_select(
            cls_from=M2M_UsersFolders.folder_id,
            where_params=[
                M2M_UsersFolders.user_id == user.id,
                M2M_UsersFolders.expired_at != None,
            ],
        )
        inner_folders: List[Folders] = await database_worker.custom_orm_select(
            cls_from=Folders, where_params=[Folders.id.in_(shared_folders_ids)]
        )
        fallback_string = "main_menu"

    markup_inline = shared_ls_k.get(
        folders=inner_folders,
        files=inner_files,
        fallback_string=fallback_string,
    )

    await callback.message.delete()
    photo = FSInputFile("src/settings.png")
    await callback.message.answer_photo(
        photo=photo,
        caption=f"🌐 {current_folder.name if current_folder_id else 'Shared Folders'}",
        reply_markup=markup_inline,
    )


@router.callback_query(F.data.startswith("shared_file_menu"))
async def shared_file_menu(callback: CallbackQuery) -> None:
    current_file_id: int = int(callback.data.split("|")[1])

    current_file: Files = await database_worker.custom_orm_select(
        cls_from=Files,
        where_params=[Files.id == current_file_id],
        get_unpacked=True,
    )
    parent_folder_id: int = await database_worker.custom_orm_select(
        cls_from=M2M_FilesFolders.folder_id,
        where_params=[M2M_FilesFolders.file_id == current_file_id],
        get_unpacked=True,
    )
    parent_folder: Folders = await database_worker.custom_orm_select(
        cls_from=Folders,
        where_params=[Folders.id == parent_folder_id],
        get_unpacked=True,
    )

    markup_inline = shared_file_menu_k.get(
        file=current_file, fallback_string=f"shared_ls|{parent_folder.id}"
    )
    await callback.message.delete()
    await callback.message.answer(
        text=f">📑 {current_file.name}",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
