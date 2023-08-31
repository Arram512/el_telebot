from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.db_api.models import DBCommander

async def payment_requests_list_keyboard():
    payment_requests_keyboard_buttons = []

    payment_requests = await DBCommander.get_payment_check_requests()
    print(payment_requests)
    for user in payment_requests:
        payment_requests_keyboard_buttons.append(InlineKeyboardButton(text = user[1], callback_data=user[0]))

    payment_requests_keyboard = InlineKeyboardMarkup(row_width=1)
    for button in payment_requests_keyboard_buttons:
        payment_requests_keyboard.add(button)

    return payment_requests_keyboard
