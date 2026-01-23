from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.enums.parse_mode import ParseMode

from config import database_engine_async, TELEGRAM_TOKEN

from keyboards.personal import personal_file_menu_k

from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_m2m_files_folders_model import M2M_FilesFolders
from database.orm.public_files_model import Files
from database.orm.public_folders_model import Folders
from utils.personal.personal_ls import send_personal_ls_menu

bot = Bot(token=TELEGRAM_TOKEN)
router = Router()
database_worker = DatabaseWorkerAsync(database_engine_async)


@router.callback_query(F.data.startswith("personal_sort_alpha"))
async def personal_sort_alpha(callback: CallbackQuery):
    current_folder_id: int = int(callback.data.split("|")[1])
    await send_personal_ls_menu(
        current_folder_id=current_folder_id,
        chat_id=callback.message.chat.id,
        message_id_to_delete=callback.message.message_id,
        bot=bot,
        database_worker=database_worker,
        do_sort_alpha=True
    )


@router.callback_query(F.data.startswith("personal_sort_data"))
async def personal_sort_data(callback: CallbackQuery):
    current_folder_id: int = int(callback.data.split("|")[1])
    await send_personal_ls_menu(
        current_folder_id=current_folder_id,
        chat_id=callback.message.chat.id,
        message_id_to_delete=callback.message.message_id,
        bot=bot,
        database_worker=database_worker,
        do_sort_data=True
    )


@router.callback_query(F.data.startswith("personal_ls"))
async def personal_ls(callback: CallbackQuery) -> None:
    current_folder_id: int = int(callback.data.split("|")[1])

    await send_personal_ls_menu(
        current_folder_id=current_folder_id,
        chat_id=callback.message.chat.id,
        message_id_to_delete=callback.message.message_id,
        bot=bot,
        database_worker=database_worker,
    )

@router.callback_query(F.data.startswith("personal_file_menu"))
async def personal_file_menu(callback: CallbackQuery) -> None:
    callback_data = callback.data.split("|")
    current_file_id: int = int(callback_data[1])

    current_file: Files = await database_worker.custom_orm_select(
        cls_from=Files,
        where_params=[Files.id == current_file_id],
        get_unpacked=True,
    )
    parent_folder_id: int = await database_worker.custom_orm_select(
        cls_from=M2M_FilesFolders.folder_id,
        where_params=[M2M_FilesFolders.file_id == current_file_id],
        get_unpacked=True,
    )
    parent_folder: Folders = await database_worker.custom_orm_select(
        cls_from=Folders,
        where_params=[Folders.id == parent_folder_id],
        get_unpacked=True,
    )

    markup_inline = personal_file_menu_k.get(
        file=current_file,
        fallback_string=f"personal_ls|{parent_folder.id}",
        parent_folder_id=parent_folder_id,
    )

    await callback.message.delete()
    await callback.message.answer(
        text=f">📑 {current_file.name}",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )
