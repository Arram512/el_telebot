from loader import dp
from aiogram.types import Message
from keyboards.default import school
from aiogram.dispatcher.filters import Command, Text

registered_users = [1111262860, 1111262861]


@dp.message_handler(Text("Հայտնության դպրոց"))
async def get_selected_module(message: Message):
    if message.from_user.id not in registered_users:
        await message.answer(f"Բարև, {message.from_user.full_name}, դուք գրանցված չեք դասընթացին!")
    else:
        await message.answer(f"Անցում հայտնության դպրոց դեպի յա յա յա", reply_markup=school)

@dp.message_handler(Text(equals=["Ադմինիստրատոր", "Սիրելի գործընկեր"]))
async def get_selected_module(message: Message):
    await message.answer(f"Անցում {message.text}")
