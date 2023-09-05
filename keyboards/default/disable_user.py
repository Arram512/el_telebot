from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

yes = "Այո"
no = "Ոչ"
cancel = "Cancel"
disable_user_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=yes),
            KeyboardButton(text=no),
            KeyboardButton(text=cancel),
        ]
    ], 
    resize_keyboard=False
)
