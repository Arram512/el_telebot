from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

yes = "Այո"
no = "Ոչ"
cancel = "Չեղարկել"
disable_user_markup = ReplyKeyboardMarkup(
    keyboard=[
            [KeyboardButton(text=yes)],
            [KeyboardButton(text=no)],
            [KeyboardButton(text=cancel)],
    ], 
    resize_keyboard=True
)
