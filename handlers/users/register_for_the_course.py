from loader import dp
from aiogram.types import Message
from keyboards.default import school
from aiogram.dispatcher.filters import Command, Text

@dp.message_handler(Text("Գրանցվել դասընթացին"))
async def get_selected_module(message: Message):
    await message.answer(text="Դե գրանցվի ինչ ես ուզում")

