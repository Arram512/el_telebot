from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from loader import dp
from states.notify_users import NotifyUsers
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from utils.db_api.models import DBCommander
from keyboards.default import disable_user_markup
from keyboards.inline import users_list_keyboard


@dp.message_handler(Text("Ուղարկել ծանուցում օգտատերերին"), state=None)
async def enter_activating_username(message: Message):
    if await DBCommander.check_if_admin(message.from_user.id):
        await message.answer(text="Ընտրեք թեման", reply_markup=await users_list_keyboard())
        await NotifyUsers.EnterUsername.set()
        
@dp.callback_query_handler(state=NotifyUsers.EnterUsername)
async def search_user(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    user_id = call.data
    search_result = await DBCommander.get_user(user_id)
    print(search_result)
    if search_result:
        await state.update_data(user_id=user_id)
        await call.message.answer(text=f"Ուղարկեք նամակը")
    await NotifyUsers.SendNotification.set()

@dp.message_handler(state=NotifyUsers.SendNotification)
async def disable_user(message: Message, state: FSMContext):
    if await DBCommander.check_if_admin(message.from_user.id):
        if message.text:
            data = await state.get_data()
            user_id = data.get("user_id")
            await dp.bot.send_message(user_id, message.text)
            await message.answer("Նամակը ուղարկված է օգտատիրոջը")
            await state.finish()
        else:
            await message.answer(text="Անթույլատրելի գործողություն")        