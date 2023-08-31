from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from loader import dp
from states.admin_disable_user import DisableUserGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from utils.db_api.models import DBCommander
from keyboards.default import disable_user_markup
from keyboards.inline import users_list_keyboard


@dp.message_handler(Text("Ապաակտիվացնել օգտատիրոջը"), state=None)
async def enter_activating_username(message: Message):
    if await DBCommander.check_if_admin(message.from_user.id):
        await message.answer(text="Ընտրեք օգտատիրոջը", reply_markup=await users_list_keyboard())
        await DisableUserGroup.EnterUsername.set()
        
@dp.callback_query_handler(state=DisableUserGroup.EnterUsername)
async def search_user(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    user_id = call.data
    search_result = await DBCommander.get_user(user_id)
    print(search_result)
    if search_result:
        await state.update_data(user_id=user_id)
        await call.message.answer(text=f"Փռթել օգտատիրոջը?", reply_markup=disable_user_markup)
    await DisableUserGroup.UserPresenceCheck.set()

@dp.message_handler(state=DisableUserGroup.UserPresenceCheck)
async def disable_user(message: Message, state: FSMContext):
    if await DBCommander.check_if_admin(message.from_user.id):
        if message.text == "Այո":
            data = await state.get_data()
            user_id = data.get("user_id")
            return_status = await DBCommander.disable_user(int(user_id))
            await message.answer(text=f"Return status  {return_status}", reply_markup=ReplyKeyboardRemove())
            await state.finish()
        elif message.text == "Ոչ":
            await message.answer(text=f"Օգտատիրոջ ակտիվացումը չեղարկվեց", reply_markup=ReplyKeyboardRemove())
            await state.finish()

        else:
            await message.answer(text="Անթույլատրելի գործողություն")        