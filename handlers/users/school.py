from loader import dp
from aiogram.types import Message
from keyboards.default import school
from aiogram.dispatcher.filters import Command, Text
from utils.db_api.models import DBCommander


@dp.message_handler(Text("Հայտնության դպրոց"))
async def get_selected_module(message: Message):
    await message.answer(f"Անցում հայտնության դպրոց դեպի յա յա յա", reply_markup=school)

@dp.message_handler(Text(equals=["Ադմինիստրատոր", "Սիրելի գործընկեր"]))
async def get_selected_module(message: Message):
    await message.answer(f"Անցում {message.text}")


