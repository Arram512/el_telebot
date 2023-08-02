from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

disable_user_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Այո"),
            KeyboardButton(text="Ոչ"),
        ]
    ], 
    resize_keyboard=False
)
