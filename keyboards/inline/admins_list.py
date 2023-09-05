from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.db_api.models import DBCommander



async def admins_list_keyboard():
    admins_list_keyboard_buttons = []

    admins_list = await DBCommander.get_admin_users_fork()
    print(admins_list)
    for user in admins_list:
        admins_list_keyboard_buttons.append(InlineKeyboardButton(text = user[1], callback_data=user[0]))

    admins_list_keyboard = InlineKeyboardMarkup(row_width=1)
    for button in admins_list_keyboard_buttons:
        admins_list_keyboard.add(button)

    return admins_list_keyboard