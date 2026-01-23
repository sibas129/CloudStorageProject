import asyncio
from config import database_engine_async
from database.oop.database_worker_async import DatabaseWorkerAsync
from database.orm import Admins
from admin_app.services.admins import columns_to_dict
import getpass

database_worker = DatabaseWorkerAsync(database_engine_async)


async def add_superadmin():
    admin_name = input("Введите username: ")
    admin_pass = getpass.getpass("Введите пароль для суперадмина: ")
    a = Admins(username=admin_name, is_superadmin=True)
    a.set_password(admin_pass)
    admin_data = [columns_to_dict(a)]
    await database_worker.custom_insert(
        cls_to=Admins,
        data=admin_data
    )

asyncio.run(add_superadmin())
