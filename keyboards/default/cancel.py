from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel = "Չեղարկել❌"

cancel_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=cancel)
        ]
    ], 
    resize_keyboard=True
)
