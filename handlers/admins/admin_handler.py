from aiogram.types import Message
from loader import dp
from keyboards.default import admin_actions, menu_for_users
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from utils.db_api.get_administrators_list import get_admins_list


@dp.message_handler(Text("Ադմինիստրատոր"))
async def get_selected_module(message: Message):
    if message.from_user.id in get_admins_list():
        await message.answer(text="Ընտրեք գործողությունը", reply_markup=admin_actions)
    else:
        await message.answer(text="Ընտրեք գործողությունը նշված ցուցակից", reply_markup=menu_for_users)
        