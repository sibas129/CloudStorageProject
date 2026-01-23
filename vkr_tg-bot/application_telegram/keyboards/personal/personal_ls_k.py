from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from typing import List

from database.orm.public_files_model import Files
from database.orm.public_folders_model import Folders


def get(
    folders: List[Folders],
    files: List[Files],
    current_folder: Folders,
    fallback_string: str,
    parent_folder_id: int = None,
) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for folder in folders:
        builder.row(
            types.InlineKeyboardButton(
                text=f"📂 {folder.name}", callback_data=f"personal_ls|{folder.id}"
            )
        )

    for file in files:
        builder.row(
            types.InlineKeyboardButton(
                text=f"📑 {file.name}", callback_data=f"personal_file_menu|{file.id}"
            )
        )

    builder.row(
        types.InlineKeyboardButton(
            text="📨 Загрузить файл", callback_data=f"upload_file|{current_folder.id}"
        ),
        types.InlineKeyboardButton(
            text="🗂 Создать папку", callback_data=f"create_folder|{current_folder.id}"
        ),
    )
    if fallback_string != "main_menu":
        delete_callback_data = f"delete_folder|{current_folder.id}"

        if parent_folder_id:
            delete_callback_data += f"|{parent_folder_id}"
        else:
            delete_callback_data += "|0"

        builder.row(
            types.InlineKeyboardButton(
                text="🗑 Удалить папку",
                callback_data=delete_callback_data,
            ),
            types.InlineKeyboardButton(
                text="👥 Поделиться папкой",
                callback_data=f"share_folder|{current_folder.id}",
            ),
        )
    builder.row(
        types.InlineKeyboardButton(text="Сорт. алфавит", callback_data=f"personal_sort_alpha|{current_folder.id}"),
        types.InlineKeyboardButton(text="Сорт. дата", callback_data=f"personal_sort_data|{current_folder.id}")
    )

    builder.row(
        types.InlineKeyboardButton(text="🔙 Назад", callback_data=f"{fallback_string}")
    )
    return builder.as_markup(resize_keyboard=True)
