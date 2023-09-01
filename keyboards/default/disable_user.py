from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

yes = "Այո"
no = "Ոչ"

disable_user_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=yes),
            KeyboardButton(text=no),
        ]
    ], 
    resize_keyboard=False
)
