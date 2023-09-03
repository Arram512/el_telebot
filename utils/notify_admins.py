import logging

from aiogram import Dispatcher
from utils.db_api.models import DBCommander


async def notify_admins(dp: Dispatcher, user_data, action):
    ADMINS = await DBCommander.get_admin_users()
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin[0], f"🔔{action}")

        except Exception as err:
            logging.exception(err)
