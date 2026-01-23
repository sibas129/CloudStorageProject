from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, BufferedInputFile, Message, FSInputFile
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from typing import List
import uuid

from config import database_engine_async, ETHERPAD_URL, TELEGRAM_TOKEN

from keyboards import delete_message_k
from keyboards.collaboration import (
    collaborations_ls_k,
    collaboration_menu_k,
    confirm_deleting_collaboration_k,
)
from utils.qr import generate_qr
from utils.notepad.notepad_worker import NotepadNamespace

from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_users_model import Users
from database.orm.public_collaborations_model import Collaborations


router = Router()
database_worker = DatabaseWorkerAsync(database_engine_async)
bot = Bot(token=TELEGRAM_TOKEN)


class CollaborationsGroup(StatesGroup):
    waiting_to_name = State()


@router.callback_query(F.data == "collaborations_ls")
async def collaborations_ls(callback: CallbackQuery) -> None:
    user: Users = await database_worker.custom_orm_select(
        cls_from=Users,
        where_params=[Users.telegram_id == callback.message.chat.id],
        get_unpacked=True,
    )
    collaborations: List[Collaborations] = await database_worker.custom_orm_select(
        cls_from=Collaborations, where_params=[Collaborations.user_id == user.id]
    )

    markup_inline = collaborations_ls_k.get(collaborations=collaborations)
    await callback.message.delete()
    photo = FSInputFile("src/calendar.png")
    await callback.message.answer_photo(
        photo=photo,
        caption=f">🌐 Список всех доступных рабочих пространств",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.callback_query(F.data.startswith("collaboration_menu"))
async def collaboration_menu(callback: CallbackQuery) -> None:
    collaboration_id = int(callback.data.split("|")[1])

    collaboration: Collaborations = await database_worker.custom_orm_select(
        cls_from=Collaborations,
        where_params=[Collaborations.id == collaboration_id],
        get_unpacked=True,
    )

    markup_inline = collaboration_menu_k.get(collaboration=collaboration)
    await callback.message.delete()
    await callback.message.answer(
        text=f">🌐 {collaboration.name}\n\n>```{ETHERPAD_URL}/p/{collaboration.uuid_name}```",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.callback_query(F.data.startswith("get_qr"))
async def get_qr(callback: CallbackQuery) -> None:
    collaboration_id = int(callback.data.split("|")[1])

    collaboration: Collaborations = await database_worker.custom_orm_select(
        cls_from=Collaborations,
        where_params=[Collaborations.id == collaboration_id],
        get_unpacked=True,
    )

    qr_result = generate_qr(url=f"{ETHERPAD_URL}/p/{collaboration.uuid_name}")
    photo = BufferedInputFile(file=qr_result.read(), filename="qr.png")

    markup_inline = delete_message_k.get()
    await callback.message.answer_photo(
        photo=photo,
        caption=f">🌐 {collaboration.name}",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.callback_query(F.data.startswith("delete_collaboration"))
async def delete_collaboration(callback: CallbackQuery) -> None:
    collaboration_id = int(callback.data.split("|")[1])

    collaboration: Collaborations = await database_worker.custom_orm_select(
        cls_from=Collaborations,
        where_params=[Collaborations.id == collaboration_id],
        get_unpacked=True,
    )

    markup_inline = confirm_deleting_collaboration_k.get(collaboration=collaboration)
    await callback.message.delete()
    await callback.message.answer(
        text=f">‼️ Вы уверены что хотите удалить данную рабочую область?",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.callback_query(F.data.startswith("ok_delete_collaboration"))
async def ok_delete_collaboration(callback: CallbackQuery) -> None:
    collaboration_id = int(callback.data.split("|")[1])

    await database_worker.custom_delete_all(
        cls_from=Collaborations, where_params=[Collaborations.id == collaboration_id]
    )
    await collaborations_ls(callback=callback)


@router.callback_query(F.data.startswith("create_collaboration"))
async def create_collaboration(callback: CallbackQuery, state: FSMContext) -> None:
    sent_message = await callback.message.answer(
        text="Введите имя для новой рабочей области:"
    )

    await state.set_state(CollaborationsGroup.waiting_to_name)
    await state.update_data(callback=callback)
    await state.update_data(id_to_delete=sent_message.message_id)


@router.message(CollaborationsGroup.waiting_to_name)
async def waiting_to_name(message: Message, state: FSMContext) -> None:
    collaboration_name = message.text
    uuid_name = str(uuid.uuid4())

    state_data = await state.get_data()
    id_to_delete = int(state_data["id_to_delete"])
    callback = state_data["callback"]

    user: Users = await database_worker.custom_orm_select(
        cls_from=Users,
        where_params=[Users.telegram_id == message.chat.id],
        get_unpacked=True,
    )

    await NotepadNamespace.create_page(name=uuid_name)

    data_to_insert = {
        "user_id": user.id,
        "name": collaboration_name,
        "uuid_name": uuid_name,
    }
    await database_worker.custom_insert(cls_to=Collaborations, data=[data_to_insert])

    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    await message.delete()
    await collaborations_ls(callback=callback)
