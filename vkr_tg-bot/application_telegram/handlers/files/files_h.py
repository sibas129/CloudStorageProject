from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery, URLInputFile, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import uuid
from io import BytesIO

from config import database_engine_async, TELEGRAM_TOKEN, S3_URL

from keyboards import delete_message_k
from utils.s3.s3_worker import S3Worker

from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_files_model import Files
from database.orm.public_m2m_files_folders_model import M2M_FilesFolders
from utils.organizations.organizations_ls import send_organization_ls_menu

from utils.personal.personal_ls import send_personal_ls_menu

router = Router()
database_worker = DatabaseWorkerAsync(database_engine_async)
s3_worker = S3Worker()
bot = Bot(token=TELEGRAM_TOKEN)


class FilesGroup(StatesGroup):
    waiting_to_name = State()
    waiting_to_file_replace = State()
    waiting_to_file_create = State()


@router.callback_query(F.data.startswith("download_file"))
async def download_file(callback: CallbackQuery) -> None:
    file_id = int(callback.data.split("|")[1])
    file: Files = await database_worker.custom_orm_select(
        cls_from=Files, where_params=[Files.id == file_id], get_unpacked=True
    )
    file = URLInputFile(
        f"{S3_URL}/rucloud/{file.path}",
        filename=f"{file.name}.{file.path.split('.')[-1]}",
    )

    markup_inline = delete_message_k.get()
    await callback.message.answer_document(
        document=file,
        caption=f"✅ Файл скачан",
        reply_markup=markup_inline,
    )


@router.callback_query(F.data.startswith("delete_file"))
async def delete_file(callback: CallbackQuery) -> None:
    callback_data = callback.data.split("|")
    file_id = int(callback_data[1])
    parent_folder_id = int(callback_data[2])
    organization_id = int(callback_data[3]) if len(callback_data) == 4 else None

    file: Files = await database_worker.custom_orm_select(
        cls_from=Files, where_params=[Files.id == file_id], get_unpacked=True
    )

    s3_worker.delete_file(path=file.path)
    await database_worker.custom_delete_all(
        cls_from=Files,
        where_params=[Files.id == file_id]
    )

    if organization_id:
        await send_organization_ls_menu(
            chat_id=callback.message.chat.id,
            message_id_to_delete=callback.message.message_id,
            current_folder_id=parent_folder_id,
            current_organization_id=organization_id,
            bot=bot,
            database_worker=database_worker,
        )
    else:
        await send_personal_ls_menu(
            chat_id=callback.message.chat.id,
            message_id_to_delete=callback.message.message_id,
            current_folder_id=parent_folder_id,
            bot=bot,
            database_worker=database_worker,
        )

    markup_inline = delete_message_k.get()
    await callback.message.answer(
        text=f"✅ Файл успешно удален",
        reply_markup=markup_inline,
    )


@router.callback_query(F.data.startswith("replace_file"))
async def replace_file(callback: CallbackQuery, state: FSMContext) -> None:
    file_id = int(callback.data.split("|")[1])

    sent_message = await callback.message.answer(
        text="Отправьте в сообщении файл без сжатия",
    )
    await state.set_state(FilesGroup.waiting_to_file_replace)
    await state.update_data(id_to_delete=sent_message.message_id)
    await state.update_data(file_id=file_id)


@router.message(FilesGroup.waiting_to_file_replace)
async def waiting_to_file_replace(message: Message, state: FSMContext) -> None:
    file_id = None

    if message.document:
        file_id = message.document.file_id
    elif message.photo:
        file_id = message.photo[-1].file_id
    elif message.video:
        file_id = message.video.file_id
    elif message.audio:
        file_id = message.audio.file_id
    elif message.voice:
        file_id = message.voice.file_id
    elif message.video_note:
        file_id = message.video_note.file_id
    elif message.animation:
        file_id = message.animation.file_id
    elif message.sticker:
        file_id = message.sticker.file_id

    if not file_id:
        await message.answer(
            text="❌ Не удалось загрузить файл",
        )
        return

    file = await bot.get_file(file_id)
    buffer = BytesIO()
    await bot.download(file, destination=buffer)
    file_bytes = buffer.getvalue()

    state_data = await state.get_data()
    id_to_delete = int(state_data["id_to_delete"])
    file_id = state_data["file_id"]

    size = file.file_size

    await database_worker.custom_orm_update(
        cls_to=Files,
        where_params=[Files.id == file_id],
        data={"size": size}
    )

    file: Files = await database_worker.custom_orm_select(
        cls_from=Files, where_params=[Files.id == file_id], get_unpacked=True
    )

    s3_worker.delete_file(path=file.path)
    s3_worker.create_file(path=file.path, content=file_bytes)

    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    await message.delete()

    markup_inline = delete_message_k.get()
    await message.answer(
        text=f"✅ Файл успешно заменен",
        reply_markup=markup_inline,
    )


@router.callback_query(F.data.startswith("upload_file"))
async def upload_file(callback: CallbackQuery, state: FSMContext) -> None:
    callback_data = callback.data.split("|")

    folder_id = int(callback_data[1])
    organization_id = int(callback_data[2]) if len(callback_data) == 3 else None

    sent_message = await callback.message.answer(
        text="Отправьте файл в сообщении без сжатия",
    )
    await state.set_state(FilesGroup.waiting_to_file_create)
    await state.update_data(id_to_delete=sent_message.message_id)
    await state.update_data(folder_id=folder_id)
    await state.update_data(menu_message_id=callback.message.message_id)
    await state.update_data(organization_id=organization_id)


@router.message(FilesGroup.waiting_to_file_create)
async def waiting_to_file_create(message: Message, state: FSMContext) -> None:
    file_id = None

    if message.document:
        file_id = message.document.file_id
    elif message.photo:
        file_id = message.photo[-1].file_id
    elif message.video:
        file_id = message.video.file_id
    elif message.audio:
        file_id = message.audio.file_id
    elif message.voice:
        file_id = message.voice.file_id
    elif message.video_note:
        file_id = message.video_note.file_id
    elif message.animation:
        file_id = message.animation.file_id
    elif message.sticker:
        file_id = message.sticker.file_id

    if not file_id:
        await message.answer(
            text="❌ Не удалось загрузить файл",
        )
        return

    file = await bot.get_file(file_id)
    buffer = BytesIO()
    await bot.download(file, destination=buffer)
    file_bytes = buffer.getvalue()
    file_extension = file.file_path.split(".")[-1]

    file_size = file.file_size

    sent_message = await message.answer(
        text="Напишите название для нового файла",
    )

    state_data = await state.get_data()
    id_to_delete = int(state_data["id_to_delete"])
    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    await message.delete()

    await state.set_state(FilesGroup.waiting_to_name)
    await state.update_data(file_bytes=file_bytes)
    await state.update_data(file_extension=file_extension)
    await state.update_data(id_to_delete=sent_message.message_id)

    await state.update_data(file_size=file_size)


@router.message(FilesGroup.waiting_to_name)
async def waiting_to_name(message: Message, state: FSMContext) -> None:
    name = message.text

    if not name or not name.replace("_", "").replace(" ", "").isalnum() or len(name) > 255:
        await message.answer(
            text="❌ Название файла должно содержать только буквы, цифры и символ подчеркивания, и не превышать 255 символов",
        )
        return

    state_data = await state.get_data()
    id_to_delete = int(state_data["id_to_delete"])
    folder_id = state_data["folder_id"]
    file_bytes = state_data["file_bytes"]
    file_extension = state_data["file_extension"]
    menu_message_id = state_data["menu_message_id"]
    organization_id = state_data["organization_id"]

    file_size = state_data["file_size"]

    file_path = str(uuid.uuid4())

    data_to_insert = {
        "name": name,
        "path": f"{file_path}.{file_extension}",
        "size": file_size
    }
    await database_worker.custom_insert(cls_to=Files, data=[data_to_insert])
    inserted_file: Files = await database_worker.custom_orm_select(
        cls_from=Files,
        where_params=[Files.path == f"{file_path}.{file_extension}"],
        get_unpacked=True,
    )
    data_to_insert = {
        "file_id": inserted_file.id,
        "folder_id": folder_id,
    }
    await database_worker.custom_insert(cls_to=M2M_FilesFolders, data=[data_to_insert])

    s3_worker.create_file(path=inserted_file.path, content=file_bytes)

    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    await message.delete()

    # Send folder menu
    if organization_id:
        await send_organization_ls_menu(
            chat_id=message.chat.id,
            message_id_to_delete=menu_message_id,
            current_folder_id=folder_id,
            current_organization_id=organization_id,
            bot=bot,
            database_worker=database_worker,
        )
    else:
        await send_personal_ls_menu(
            chat_id=message.chat.id,
            message_id_to_delete=menu_message_id,
            current_folder_id=folder_id,
            bot=bot,
            database_worker=database_worker,
        )

    markup_inline = delete_message_k.get()
    await message.answer(
        text=f"✅ Файл успешно создан",
        reply_markup=markup_inline,
    )

