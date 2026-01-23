from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from database.orm.public_organizations_model import Organizations


def get(organization: Organizations, is_owner: bool) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text=f"📂 Файлы организации",
            callback_data=f"organizations_ls|0|{organization.id}",
        ),
    )

    if is_owner:
        builder.row(
            types.InlineKeyboardButton(
                text=f"👥 Добавить участника",
                callback_data=f"share_organization|{organization.id}",
            ),
            types.InlineKeyboardButton(
                text=f"🗑 Удалить участника",
                callback_data=f"delete_organization_member|{organization.id}",
            ),
        )
        builder.row(
            types.InlineKeyboardButton(
                text=f"🗑 Удалить организацию",
                callback_data=f"delete_organization|{organization.id}",
            ),
        )

    builder.row(
        types.InlineKeyboardButton(text="🔙 Назад", callback_data=f"organizations_list")
    )
    return builder.as_markup(resize_keyboard=True)
