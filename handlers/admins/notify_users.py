from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from loader import dp
from states.admin_disable_user import DisableUserGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from utils.db_api.models import DBCommander
from keyboards.default import disable_user_markup
from keyboards.inline import users_list_keyboard

@dp.message_handler(Text("Ակտիվացնել օգտատիրոջը"), state=None)
async def enter_activating_username(message: Message):
    if await DBCommander.check_if_admin(message.from_user.id):
        await message.answer(text="Ընտրեք օգտատիրոջը", reply_markup=await users_list_keyboard())
        await EnableUserGroup.EnterUsername.set()