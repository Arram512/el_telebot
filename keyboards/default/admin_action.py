from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_actions = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Ակտիվացնել օգտատիրոջը")],
        [KeyboardButton(text="Ապաակտիվացնել օգտատիրոջը")],
        [KeyboardButton(text="Հաստատել վճարումը")],
        [KeyboardButton(text="Ուղարկել ծանուցում")],
        [KeyboardButton(text="Հաստատել տնային աշխատանքը")],
    ], 
    resize_keyboard=True
)

superadmin_actions = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Ակտիվացնել օգտատիրոջը")],
        [KeyboardButton(text="Ապաակտիվացնել օգտատիրոջը")],
        [KeyboardButton(text="Հաստատել վճարումը")],
        [KeyboardButton(text="Հաստատել տնային աշխատանքը")],
        [KeyboardButton(text="Ուղարկել ծանուցում բոլորին")],
        [KeyboardButton(text="Ուղարկել ծանուցում ադմինիստրատորներին")],
        [KeyboardButton(text="Ուղարկել ծանուցում օգտատերերին")],
        [KeyboardButton(text="Ավելացնել ադմինիստրատոր")],
        [KeyboardButton(text="Հեռացնել ադմինիստրատորին")],
    ], 
    resize_keyboard=True  
)
