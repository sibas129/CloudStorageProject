from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


from database.orm.public_collaborations_model import Collaborations


def get(collaboration: Collaborations) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад", callback_data=f"collaboration_menu|{collaboration.id}"
        ),
        types.InlineKeyboardButton(
            text="✅ Да", callback_data=f"ok_delete_collaboration|{collaboration.id}"
        ),
    )
    return builder.as_markup(resize_keyboard=True)
