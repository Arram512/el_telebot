from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.db_api.models import DBCommander

async def homework_approve_requests_keyboard():
    homework_approve_requests_keyboard_buttons = []

    homework_approve_requests = await DBCommander.get_homework_approve_requests()
    print(homework_approve_requests)
    for user in homework_approve_requests:
        homework_approve_requests_keyboard_buttons.append(InlineKeyboardButton(text = user[1], callback_data=user[0]))

    homework_approve_requests_keyboard = InlineKeyboardMarkup(row_width=1)
    for button in homework_approve_requests_keyboard_buttons:
        homework_approve_requests_keyboard.add(button)

    return homework_approve_requests_keyboard
