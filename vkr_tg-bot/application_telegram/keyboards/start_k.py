from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


def get() -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="📂 Личные файлы", callback_data=f"personal_ls|0"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="📣 Общий доступ", callback_data=f"shared_ls|0"
        ),
        types.InlineKeyboardButton(
            text="🏣 Организации", callback_data=f"organizations_list"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🌐 Rucloud docs", callback_data=f"collaborations_ls"
        ),
    )
    return builder.as_markup(resize_keyboard=True)
