from aiogram import Bot, Dispatcher

import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import TELEGRAM_TOKEN
from handlers.collaboration import collaborations_h
from handlers.files import files_h
from handlers.folders import folders_h
from handlers.organizations import organizations_h
from handlers.personal import personal_h
from handlers.shared import shared_h
from handlers import commands_h, main_h

from schedulers.auto_check_expires import auto_check_expires

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()


async def main() -> None:
    scheduler.add_job(auto_check_expires, trigger="interval", minutes=60)
    dp.include_routers(
        commands_h.router,
        main_h.router,
        personal_h.router,
        files_h.router,
        folders_h.router,
        shared_h.router,
        organizations_h.router,
        collaborations_h.router,
    )
    await bot.delete_webhook(drop_pending_updates=True)

    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
