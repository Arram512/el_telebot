from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from loader import dp
from states.add_administrator import AddAdministrator
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from utils.db_api.models import DBCommander
from keyboards.default import disable_user_markup
from keyboards.inline import users_list_keyboard
from time import sleep


@dp.message_handler(Text("Ավելացնել ադմինիստրատոր"), state=None)
async def enter_activating_username(message: Message):
    if await DBCommander.check_if_admin(message.from_user.id):
        await message.answer(text="Ընտրեք օգտատիրոջը", reply_markup=await users_list_keyboard())
        await AddAdministrator.EnterUsername.set()
        
@dp.callback_query_handler(state=AddAdministrator.EnterUsername)
async def search_user(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    user_id = call.data
    search_result = await DBCommander.get_user(user_id)
    print(search_result)
    if search_result:
        await state.update_data(user_id=user_id)
        await call.message.answer(text=f"Հեռացնել ադմինիստրատորին", reply_markup=disable_user_markup)
    await AddAdministrator.UserPresenceCheck.set()

@dp.message_handler(state=AddAdministrator.UserPresenceCheck)
async def enable_user(message: Message, state: FSMContext):
    if await DBCommander.check_if_admin(message.from_user.id):
        if message.text == "Այո":
            data = await state.get_data()
            user_id = data.get("user_id")
            return_status = await DBCommander.add_admin(int(user_id))
            
            await message.answer(text=f"Ավելացված է նոր ադմինիստրատոր", reply_markup=ReplyKeyboardRemove())
            await state.finish()
        elif message.text == "Ոչ":
            await message.answer(text=f"Գործողությունը չեղարկվեց", reply_markup=ReplyKeyboardRemove())
            await state.finish()

        else:
            await message.answer(text="Անթույլատրելի գործողություն")