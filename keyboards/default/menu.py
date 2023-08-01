from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_for_admins = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Հայտնության դպրոց"),
            KeyboardButton(text="Ադմինիստրատոր"),
            KeyboardButton(text="Սիրելի գործընկեր")
        ]
    ], 
    resize_keyboard=True
)

menu_for_users = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Հայտնության դպրոց"),
            KeyboardButton(text="Սիրելի գործընկեր")
        ]
    ], 
    resize_keyboard=True
)