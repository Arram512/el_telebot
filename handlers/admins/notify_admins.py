from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from loader import dp
from states.notify_admins import NotifyAdmins
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from utils.db_api.models import DBCommander
from keyboards.default import disable_user_markup
from keyboards.inline import users_list_keyboard

@dp.message_handler(Text("Ուղարկել ծանուցում ադմինիստրատորներին"), state=None)
async def enter_activating_username(message: Message):
    if await DBCommander.check_if_admin(message.from_user.id):
        await message.answer(text="Ուղարկեք նամակը")
        await NotifyAdmins.SendNotification.set()

@dp.message_handler(state=NotifyAdmins.SendNotification)
async def disable_user(message: Message, state: FSMContext):
    if await DBCommander.check_if_admin(message.from_user.id):
        if message.text:
            admins = await DBCommander.get_admin_users()
            print(admins)
            for admin in admins:
                
                if int(admin[0]) != int(message.from_user.id):
                    await dp.bot.send_message(admin[0], message.text)

            await message.answer("Նամակը ուղարկված է ադմինիստրատորներին")
            await state.finish()
        else:
            await message.answer(text="Անթույլատրելի գործողություն")
