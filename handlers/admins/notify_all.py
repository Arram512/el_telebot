from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from loader import dp
from states.notify_all import NotifyAll
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from utils.db_api.models import DBCommander
from utils import notify_users
from keyboards.default import disable_user_markup
from keyboards.inline import users_list_keyboard

@dp.message_handler(Text("Ուղարկել ծանուցում բոլորին"), state=None)
async def enter_activating_username(message: Message):
    if await DBCommander.check_if_admin(message.from_user.id):
        await message.answer(text="Ուղարկեք նամակը")
        await NotifyAll.SendNotification.set()



@dp.message_handler(state=NotifyAll.SendNotification)
async def disable_user(message: Message, state: FSMContext):
    if await DBCommander.check_if_admin(message.from_user.id):
        if message.text:
            
            await notify_users(dp,str(message.text))
            await message.answer("Նամակը ուղարկված է օգտատերերին")
            await state.finish()
        else:
            await message.answer(text="Անթույլատրելի գործողություն")