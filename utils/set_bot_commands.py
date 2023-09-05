from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Ակտիվացնել բոտը"),
            types.BotCommand("help", "Օգնություն"),
            types.BotCommand("menu", "Մենյու"),
            types.BotCommand("cancel", "Չեղարկել"),
            types.BotCommand("send_payment", "Ուղարկել վճարման հաստատման հայտ"),
        ]
    )
