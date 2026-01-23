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
    organization_id: int,
) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for folder in folders:
        builder.row(
            types.InlineKeyboardButton(
                text=f"📂 {folder.name}",
                callback_data=f"organizations_ls|{folder.id}|{organization_id}",
            )
        )

    for file in files:
        builder.row(
            types.InlineKeyboardButton(
                text=f"📑 {file.name}",
                callback_data=f"organizations_file_menu|{file.id}|{organization_id}",
            )
        )

    builder.row(
        types.InlineKeyboardButton(
            text="📨 Загрузить файл", callback_data=f"upload_file|{current_folder.id}|{organization_id}"
        ),
        types.InlineKeyboardButton(
            text="🗂 Создать папку", callback_data=f"create_folder|{current_folder.id}|{organization_id}"
        ),
    )

    builder.row(
        types.InlineKeyboardButton(text="Сорт. алфавит", callback_data=f"org_sort_alpha|{current_folder.id}|{organization_id}"),
        types.InlineKeyboardButton(text="Сорт. дата", callback_data=f"org_sort_data|{current_folder.id}|{organization_id}")
    )

    builder.row(
        types.InlineKeyboardButton(text="🔙 Назад", callback_data=f"{fallback_string}")
    )
    return builder.as_markup(resize_keyboard=True)
