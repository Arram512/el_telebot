import logging

from aiogram import Dispatcher
from utils.db_api.models import DBCommander


async def notify_users(dp: Dispatcher, user_data, action):
    users = await DBCommander.get_non_admin_users()
    print(users)
    for user in notify_users:
        try:
            await dp.bot.send_message(user[0], f"🔔{action}")

        except Exception as err:
            logging.exception(err)
