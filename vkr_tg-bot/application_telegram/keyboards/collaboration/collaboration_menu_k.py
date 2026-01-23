from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


from database.orm.public_collaborations_model import Collaborations


def get(collaboration: Collaborations) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="🔗 Сгенерировать QR для доступа",
            callback_data=f"get_qr|{collaboration.id}",
        ),
        types.InlineKeyboardButton(
            text="🗑 Удалить рабочую область",
            callback_data=f"delete_collaboration|{collaboration.id}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(text="🔙 Назад", callback_data=f"collaborations_ls")
    )
    return builder.as_markup(resize_keyboard=True)
