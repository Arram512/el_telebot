from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.set_bot_commands import set_default_commands
from utils.db_api import models
import sys


async def on_startup(dispatcher):

    await models.create_db()




    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
