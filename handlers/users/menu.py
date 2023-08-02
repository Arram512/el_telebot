from loader import dp
from aiogram.types import Message
from keyboards.default import menu_for_users
from keyboards.default import menu_for_admins
from aiogram.dispatcher.filters import Command, Text
from utils.db_api.models import DBCommander


@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    if await DBCommander.check_if_admin(message.from_user.id):
        await message.answer("Ընտրեք անհրաժեշտ բաժինը", reply_markup=menu_for_admins)
    else:
        await message.answer("Ընտրեք անհրաժեշտ բաժինը", reply_markup=menu_for_users)


