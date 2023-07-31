from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Հայտնության դպրոց"),
            KeyboardButton(text="Ադմինիստրատոր"),
            KeyboardButton(text="Սիրելի գործընկեր")
        ]
    ], 
    resize_keyboard=True
)
