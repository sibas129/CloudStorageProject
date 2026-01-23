from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from keyboards import only_to_main_k
from handlers.commands_h import start_command


router = Router()


async def sth_error(message: Message, error_text: str) -> None:
    markup_inline = only_to_main_k.get()
    await message.answer(
        text=f"⛔️ Что-то пошло не так\n\nТекст ошибки: {error_text}",
        reply_markup=markup_inline,
    )


@router.callback_query(F.data == "main_menu")
async def main_menu(callback: CallbackQuery) -> None:
    await callback.message.delete()
    await start_command(callback.message)


@router.callback_query(F.data == "delete_message")
async def main_menu(callback: CallbackQuery) -> None:
    await callback.message.delete()
