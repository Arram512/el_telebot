from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.db_api.models import DBCommander

async def courses_keyboard():
    courses_keyboard_buttons = []

    courses = await DBCommander.get_courses()
    print(courses)
    for course in courses:
        courses_keyboard_buttons.append(InlineKeyboardButton(text = course, callback_data=course))

    courses_keyboard = InlineKeyboardMarkup(row_width=1)
    for button in courses_keyboard_buttons:
        courses_keyboard.add(button)

    return courses_keyboard
