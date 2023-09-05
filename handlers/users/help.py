from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Հրամանների ցուցակ: ",
            "/start - Ակտիվացնել դպրոցը",
            "/help - Ստանալ հրամանների ցուցակը",
            "/menu - Գլխավոր մենյու",
            "/send payment - Ուղարկել վճարման հաստատման հայտ"
            )
    
    await message.answer("\n".join(text))
