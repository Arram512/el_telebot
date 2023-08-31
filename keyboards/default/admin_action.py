from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_actions = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Ակտիվացնել օգտատիրոջը"),
            KeyboardButton(text="Ապաակտիվացնել օգտատիրոջը"),
            KeyboardButton(text="Հաստատել վճարումը"),
            KeyboardButton(text="Ուղարկել ծանուցում"),
        ]
    ], 
    resize_keyboard=True
)
