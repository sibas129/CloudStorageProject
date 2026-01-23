import json

from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from typing import List

from database.orm import Files
from database.orm.public_folders_model import Folders


def get(
    folders: List[Folders],
    files: List[Files],
    fallback_string: str,
) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for folder in folders:
        builder.row(
            types.InlineKeyboardButton(
                text=f"📂 {folder.name}", callback_data=f"shared_ls|{folder.id}"
            )
        )

    for file in files:
        builder.row(
            types.InlineKeyboardButton(
                text=f"📑 {file.name}", callback_data=f"shared_file_menu|{file.id}"
            )
        )

    builder.row(
        types.InlineKeyboardButton(text="🔙 Назад", callback_data=f"{fallback_string}")
    )
    return builder.as_markup(resize_keyboard=True)
