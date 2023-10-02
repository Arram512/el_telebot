from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Բարև, {message.from_user.full_name}, բարի վերադարձ!")
    await message.answer(f"Նախքան օգտագործելը ծանոթացեք բոտի ձեռնարկին\n{https://youtu.be/EPE_ltWvgk8?si=X6iXz54DDCylA6dh}")
