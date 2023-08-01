from loader import dp
from aiogram.types import Message
from keyboards.default import menu_for_users
from keyboards.default import menu_for_admins
from aiogram.dispatcher.filters import Command, Text
from utils.db_api.get_administrators_list import get_admins_list


@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    if message.from_user.id in get_admins_list():
        await message.answer("Ընտրեք անհրաժեշտ բաժինը", reply_markup=menu_for_admins)
    else:
        await message.answer("Ընտրեք անհրաժեշտ բաժինը", reply_markup=menu_for_users)


