from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


from database.orm.public_organizations_model import Organizations


def get(organization: Organizations) -> ReplyKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="🔙 Назад", callback_data=f"organization_menu|{organization.id}"
        ),
        types.InlineKeyboardButton(
            text="✅ Да", callback_data=f"ok_delete_organization|{organization.id}"
        ),
    )
    return builder.as_markup(resize_keyboard=True)
