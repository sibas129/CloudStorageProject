from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.enums.parse_mode import ParseMode

from keyboards import start_k

from utils.func_utils import auto_registration

router = Router()


@router.message(Command("start"))
async def start_command(message: Message) -> None:
    await auto_registration(message)
    markup_inline = start_k.get()
    photo = FSInputFile("src/main.png")
    await message.answer_photo(
        photo=photo,
        caption=(
            "> ☁️ Это RuCloud \- сервис, созданный для хранения данных и обмена ими "
            "с коллегами по работе\. Помимо прочего в данном приложении можно также создать совместную рабочую область "
            "и сохранить ее в свои личные файлы по завершении, после этого данным файлом можно будет поделиться с "
            "другими пользователями, так же как и любым другим\."
        ),
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.message(Command("get_id"))
async def get_id_command(message: Message) -> None:
    await auto_registration(message)
    await message.answer(
        text=(
            ">Ваш уникальный id \(вы можете скопировать и отправить его любому другому человеку, "
            "чтобы он смог предоставить вам доступ к своим файлам, папкам, или добавить "
            f"вас в организацию\): ```{message.chat.id}```"
        ),
        parse_mode=ParseMode.MARKDOWN_V2,
    )
