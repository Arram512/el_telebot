from aiogram.types import Message
from loader import dp
from states.admin_disable_user import DisableUserGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from utils.db_api.get_administrators_list import get_admins_list
from utils.db_api.search_user_in_db import search_user_in_db
from utils.db_api.models import DBCommander
from keyboards.default import disable_user_markup


@dp.message_handler(Text("Ապաակտիվացնել օգտատիրոջը"), state=None)
async def enter_activating_username(message: Message):
    if await DBCommander.check_if_admin(message.from_user.id):
        await message.answer(text="Ընտրեք օգտատիրոջը", reply_markup=)
        await DisableUserGroup.EnterUsername.set()
        
@dp.message_handler(state=DisableUserGroup.EnterUsername)
async def search_user(message: Message, state: FSMContext):
    if await DBCommander.check_if_admin(message.from_user.id):
        user_data = message.text
        search_result = await DBCommander.get_user(user_data)
        print(search_result)
        if search_result:
            await state.update_data(username=user_data)
            await message.answer(text=f"{search_result}", reply_markup=disable_user_markup)
        await DisableUserGroup.UserPresenceCheck.set()

@dp.message_handler(state=DisableUserGroup.UserPresenceCheck)
async def disable_user(message: Message, state: FSMContext):
    if await DBCommander.check_if_admin(message.from_user.id):
        if message.text == "Այո":
            data = await state.get_data()
            user_id = data.get("username")
            #return_status =
            await message.answer(text=f"Return status  {user_id}")
        await DisableUserGroup.DisableUser.set()
        