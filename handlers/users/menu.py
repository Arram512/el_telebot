from loader import dp
from aiogram.types import Message
from keyboards.default import menu
from aiogram.dispatcher.filters import Command, Text

@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer("Ընտրեք անհրաժեշտ բաժինը", reply_markup=menu)

@dp.message_handler(Text(equals=["Հայտնության դպրոց", "Ադմինիստրատոր", "Սիրելի գործընկեր"]))
async def get_selected_module(message: Message):
    await message.answer(f"Անցում {message.text}")
