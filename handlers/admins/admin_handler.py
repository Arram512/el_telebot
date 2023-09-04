from aiogram.types import Message
from loader import dp
from keyboards.default import admin_actions, menu_for_users, superadmin_actions
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from utils.db_api.models import DBCommander
from states.admin_states import AdminStates

@dp.message_handler(Text("Ադմինիստրատոր"))
async def get_selected_module(message: Message):
    if await DBCommander.check_if_admin(message.from_user.id):
        if await DBCommander.check_if_superadmin(message.from_user.id):
            await message.answer(text="Ընտրեք գործողությունը", reply_markup=superadmin_actions)
        else:
            await message.answer(text="Ընտրեք գործողությունը", reply_markup=admin_actions)
            #AdminStates.StartAdminAction.set()
    else:
        await message.answer(text="Ընտրեք գործողությունը նշված ցուցակից", reply_markup=menu_for_users)
        