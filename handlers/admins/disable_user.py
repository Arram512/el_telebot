from aiogram.types import Message
from loader import dp
from states.admin_disable_user import DisableUserGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from utils.db_api.get_administrators_list import get_admins_list
from utils.db_api.search_user_in_db import search_user_in_db


@dp.message_handler(Text("Ապաակտիվացնել օգտատիրոջը"), state=None)
async def enter_activating_username(message: Message):
    if message.from_user.id in get_admins_list():
        await message.answer(text="Ուղարկեք օգտատիրոջ այդին կամ username-ը",)
        await DisableUserGroup.EnterUsername.set()
        
@dp.message_handler(state=DisableUserGroup.EnterUsername)
async def search_user(message: Message, state: FSMContext):
    if message.from_user.id in get_admins_list():
        user_data = message.text
        search_result = search_user_in_db(user_data)
        print(search_result)
        await message.answer(text="Ուղարկեք օգտատիրոջ այդին կամ անուն ազգանունը",)
        await DisableUserGroup.UserPresenceCheck.set()
        