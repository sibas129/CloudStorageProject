from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from database.orm.public_files_model import Files


def get(file: Files, fallback_string: str, parent_folder_id: int, organization_id: int) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="🗳 Загрузить файл", callback_data=f"download_file|{file.id}|"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="♻️ Заменить файл", callback_data=f"replace_file|{file.id}"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🗑 Удалить файл", callback_data=f"delete_file|{file.id}|{parent_folder_id}|{organization_id}"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(text="🔙 Назад", callback_data=f"{fallback_string}")
    )
    return builder.as_markup(resize_keyboard=True)
