from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.db_api.models import DBCommander

async def users_list_keyboard():
    users_list_keyboard_buttons = []

    users_list = await DBCommander.get_non_admin_users()
    print(users_list)
    for user in users_list:
        users_list_keyboard_buttons.append(InlineKeyboardButton(text = user[1], callback_data=user[0]))

    users_list_keyboard = InlineKeyboardMarkup(row_width=1)
    for button in users_list_keyboard_buttons:
        users_list_keyboard.add(button)

    return users_list_keyboard

