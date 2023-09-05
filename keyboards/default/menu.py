from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_for_admins = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Հայտնության դպրոց"),
            KeyboardButton(text="Ադմինիստրատոր"),
        ]
    ], 
    resize_keyboard=True
)

menu_for_users = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Հայտնության դպրոց"),
            KeyboardButton(text="Հետադարձ կապ"),

        ]
    ], 
    resize_keyboard=True
)