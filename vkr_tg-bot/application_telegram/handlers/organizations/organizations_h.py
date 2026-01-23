from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from typing import List
import uuid

from config import database_engine_async, TELEGRAM_TOKEN
from keyboards import delete_message_k

from keyboards.organizations import (
    organization_menu_k,
    organizations_file_menu_k,
    organizations_list_k,
    confirm_deliting_organization_k,
)
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm.public_users_model import Users
from database.orm.public_organizations_model import Organizations
from database.orm.public_m2m_users_organizations_model import M2M_UsersOrganizations
from database.orm.public_m2m_organizations_folders_model import M2M_OrganizationsFolders
from database.orm.public_m2m_files_folders_model import M2M_FilesFolders
from database.orm.public_folders_model import Folders
from database.orm.public_files_model import Files

from utils.organizations.organizations_ls import send_organization_ls_menu


router = Router()
database_worker = DatabaseWorkerAsync(database_engine_async)
bot = Bot(token=TELEGRAM_TOKEN)


class OrganizationsGroup(StatesGroup):
    waiting_to_name = State()
    waiting_to_user_id_to_add = State()
    waiting_to_user_id_to_delete = State()


@router.callback_query(F.data == "organizations_list")
async def organizations_list(callback: CallbackQuery) -> None:
    user: Users = await database_worker.custom_orm_select(
        cls_from=Users,
        where_params=[Users.telegram_id == callback.message.chat.id],
        get_unpacked=True,
    )
    organizations_ids: List[int] = await database_worker.custom_orm_select(
        cls_from=M2M_UsersOrganizations.organization_id,
        where_params=[M2M_UsersOrganizations.user_id == user.id],
    )
    organizations: List[Organizations] = await database_worker.custom_orm_select(
        cls_from=Organizations,
        where_params=[
            Organizations.id.in_(organizations_ids),
            Organizations.is_deleted == False,
        ],
    )

    markup_inline = organizations_list_k.get(organizations=organizations)
    await callback.message.delete()
    photo = FSInputFile("src/organizations.png")
    await callback.message.answer_photo(
        photo=photo,
        caption=f">🏣 Список всех доступных организаций",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.callback_query(F.data.startswith("organization_menu"))
async def organization_menu(callback: CallbackQuery) -> None:
    organization_id = int(callback.data.split("|")[1])

    user: Users = await database_worker.custom_orm_select(
        cls_from=Users,
        where_params=[Users.telegram_id == callback.message.chat.id],
        get_unpacked=True,
    )
    organization: Organizations = await database_worker.custom_orm_select(
        cls_from=Organizations,
        where_params=[Organizations.id == organization_id],
        get_unpacked=True,
    )

    markup_inline = organization_menu_k.get(
        organization=organization,
        is_owner=True if organization.user_id == user.id else False,
    )
    await callback.message.delete()
    await callback.message.answer(
        text=f">🏣 {organization.name}",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.callback_query(F.data.startswith("org_sort_alpha"))
async def org_sort_alpha(callback: CallbackQuery) -> None:
    current_folder_id: int = int(callback.data.split("|")[1])
    current_organization_id: int = int(callback.data.split("|")[2])

    await send_organization_ls_menu(
        chat_id=callback.message.chat.id,
        message_id_to_delete=callback.message.message_id,
        current_folder_id=current_folder_id,
        current_organization_id=current_organization_id,
        bot=bot,
        database_worker=database_worker,
        do_sort_alpha=True,
    )


@router.callback_query(F.data.startswith("org_sort_data"))
async def org_sort_data(callback: CallbackQuery) -> None:
    current_folder_id: int = int(callback.data.split("|")[1])
    current_organization_id: int = int(callback.data.split("|")[2])

    await send_organization_ls_menu(
        chat_id=callback.message.chat.id,
        message_id_to_delete=callback.message.message_id,
        current_folder_id=current_folder_id,
        current_organization_id=current_organization_id,
        bot=bot,
        database_worker=database_worker,
        do_sort_data=True,
    )


@router.callback_query(F.data.startswith("organizations_ls"))
async def organizations_ls(callback: CallbackQuery) -> None:
    current_folder_id: int = int(callback.data.split("|")[1])
    current_organization_id: int = int(callback.data.split("|")[2])

    await send_organization_ls_menu(
        chat_id=callback.message.chat.id,
        message_id_to_delete=callback.message.message_id,
        current_folder_id=current_folder_id,
        current_organization_id=current_organization_id,
        bot=bot,
        database_worker=database_worker,
    )


@router.callback_query(F.data.startswith("organizations_file_menu"))
async def organizations_file_menu(callback: CallbackQuery) -> None:
    callback_data = callback.data.split("|")
    current_file_id: int = int(callback_data[1])
    current_organization_id: int = int(callback_data[2])

    current_file: Files = await database_worker.custom_orm_select(
        cls_from=Files, where_params=[Files.id == current_file_id], get_unpacked=True
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

    markup_inline = organizations_file_menu_k.get(
        file=current_file,
        fallback_string=f"organizations_ls|{parent_folder.id}|{current_organization_id}",
        parent_folder_id=parent_folder.id,
        organization_id=current_organization_id,
    )
    await callback.message.delete()
    await callback.message.answer(
        text=f">📑 {current_file.name}",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.callback_query(F.data.startswith("create_organization"))
async def create_organization(callback: CallbackQuery, state: FSMContext) -> None:
    sent_message = await callback.message.answer(
        text="Введите имя для новой организации"
    )
    await state.set_state(OrganizationsGroup.waiting_to_name)
    await state.update_data(callback=callback)
    await state.update_data(id_to_delete=sent_message.message_id)


@router.message(OrganizationsGroup.waiting_to_name)
async def waiting_to_name(message: Message, state: FSMContext):
    organization_name = message.text
    state_data = await state.get_data()
    id_to_delete = int(state_data["id_to_delete"])
    callback = state_data["callback"]

    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    await message.delete()

    user: Users = await database_worker.custom_orm_select(
        cls_from=Users,
        where_params=[Users.telegram_id == message.chat.id],
        get_unpacked=True,
    )

    data_to_insert = {
        "user_id": user.id,
        "name": organization_name,
    }
    await database_worker.custom_insert(cls_to=Organizations, data=[data_to_insert])

    organization: Organizations = await database_worker.custom_orm_select(
        cls_from=Organizations,
        where_params=[Organizations.name == organization_name],
        order_by=[Organizations.created_at.desc()],
        sql_limit=1,
        get_unpacked=True,
    )

    data_to_insert = {"user_id": user.id, "organization_id": organization.id}
    await database_worker.custom_insert(
        cls_to=M2M_UsersOrganizations, data=[data_to_insert]
    )

    random_name = str(uuid.uuid4())

    data_to_insert = {
        "name": random_name,
    }
    await database_worker.custom_insert(cls_to=Folders, data=[data_to_insert])

    folder: Folders = await database_worker.custom_orm_select(
        cls_from=Folders,
        where_params=[Folders.name == random_name],
        order_by=[Folders.created_at.desc()],
        sql_limit=1,
        get_unpacked=True,
    )

    data_to_insert = {
        "organization_id": organization.id,
        "folder_id": folder.id,
        "is_root": True,
    }
    await database_worker.custom_insert(
        cls_to=M2M_OrganizationsFolders, data=[data_to_insert]
    )

    await organizations_list(callback=callback)


@router.callback_query(F.data.startswith("share_organization"))
async def share_organization(callback: CallbackQuery, state: FSMContext) -> None:
    organization_id: int = int(callback.data.split("|")[1])
    sent_message = await callback.message.answer(text="Введите никнейм участника")
    await state.set_state(OrganizationsGroup.waiting_to_user_id_to_add)
    await state.update_data(callback=callback)
    await state.update_data(id_to_delete=sent_message.message_id)
    await state.update_data(organization_id=organization_id)


@router.message(OrganizationsGroup.waiting_to_user_id_to_add)
async def waiting_to_user_id_to_add(message: Message, state: FSMContext):
    user_name = message.text
    state_data = await state.get_data()
    id_to_delete = int(state_data["id_to_delete"])
    callback = state_data["callback"]
    organization_id = state_data["organization_id"]

    if user_name[0] == "@":
        user_name = user_name[1:]

    user: Users = await database_worker.custom_orm_select(
        cls_from=Users, where_params=[Users.telegram_name == user_name], get_unpacked=True
    )

    if user:
        data_to_insert = {
            "user_id": user.id,
            "organization_id": organization_id,
        }

        # check if user already in organization
        user_organization: M2M_UsersOrganizations = await database_worker.custom_orm_select(
            cls_from=M2M_UsersOrganizations,
            where_params=[
                M2M_UsersOrganizations.user_id == user.id,
                M2M_UsersOrganizations.organization_id == organization_id,
            ],
            get_unpacked=True,
        )

        if user_organization:
            await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
            await message.delete()

            markup_inline = delete_message_k.get()
            await message.answer(
                text=f"❌ Пользователь уже добавлен в организацию",
                reply_markup=markup_inline,
            )

            await organizations_list(callback=callback)
            return

        await database_worker.custom_insert(
            cls_to=M2M_UsersOrganizations, data=[data_to_insert]
        )

    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    await message.delete()

    markup_inline = delete_message_k.get()
    await message.answer(
        text=f"✅ Пользователь успешно добавлен в организацию",
        reply_markup=markup_inline,
    )

    await organizations_list(callback=callback)


@router.callback_query(F.data.startswith("delete_organization_member"))
async def delete_organization_member(callback: CallbackQuery, state: FSMContext) -> None:
    organization_id: int = int(callback.data.split("|")[1])
    sent_message = await callback.message.answer(text="Введите никнейм участника")
    await state.set_state(OrganizationsGroup.waiting_to_user_id_to_delete)
    await state.update_data(callback=callback)
    await state.update_data(id_to_delete=sent_message.message_id)
    await state.update_data(organization_id=organization_id)


@router.message(OrganizationsGroup.waiting_to_user_id_to_delete)
async def waiting_to_user_id_to_delete(message: Message, state: FSMContext):
    user_telegram_name = message.text
    state_data = await state.get_data()
    id_to_delete = int(state_data["id_to_delete"])
    callback = state_data["callback"]
    organization_id = state_data["organization_id"]

    if user_telegram_name[0] == "@":
        user_telegram_name = user_telegram_name[1:]

    user: Users = await database_worker.custom_orm_select(
        cls_from=Users, where_params=[Users.telegram_name == user_telegram_name], get_unpacked=True
    )

    if user:
        await database_worker.custom_delete_all(
            cls_from=M2M_UsersOrganizations,
            where_params=[
                M2M_UsersOrganizations.user_id == user.id,
                M2M_UsersOrganizations.organization_id == organization_id,
            ],
        )

    await bot.delete_message(chat_id=message.chat.id, message_id=id_to_delete)
    await message.delete()

    markup_inline = delete_message_k.get()
    await message.answer(
        text=f"✅ Пользователь успешно удален из организации",
        reply_markup=markup_inline,
    )

    await organizations_list(callback=callback)


@router.callback_query(F.data.startswith("delete_organization"))
async def delete_organization(callback: CallbackQuery) -> None:
    organization_id = int(callback.data.split("|")[1])
    organization: Organizations = await database_worker.custom_orm_select(
        cls_from=Organizations,
        where_params=[Organizations.id == organization_id],
        get_unpacked=True,
    )

    markup_inline = confirm_deliting_organization_k.get(organization=organization)
    await callback.message.answer(
        text=f">‼️ Вы уверены что хотите удалить данную организацию?",
        reply_markup=markup_inline,
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@router.callback_query(F.data.startswith("ok_delete_organization"))
async def ok_delete_organization(callback: CallbackQuery) -> None:
    organization_id = int(callback.data.split("|")[1])
    await database_worker.custom_delete_all(
        cls_from=Organizations, where_params=[Organizations.id == organization_id]
    )
    await organizations_list(callback=callback)
