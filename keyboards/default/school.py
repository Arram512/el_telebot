from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api.models import DBCommander



async def course_themes(course):
    course_themes_buttons = []
    tempset = []
    course_themes = await DBCommander.get_course_themes(course)
    for theme in course_themes:
        if theme not in tempset:
            tempset.append(theme)
            course_themes_buttons.append(InlineKeyboardButton(text = theme[0], callback_data=theme[0]))

    course_themes_buttons.append(InlineKeyboardButton(text = "Վերադարձ", callback_data='back'))
    course_themes_keyboard = InlineKeyboardMarkup(row_width=1)
    for button in course_themes_buttons:
        course_themes_keyboard.add(button)


    return course_themes_keyboard



async def lesson_content(theme):
    course_lessons_buttons = []

    course_lessons = await DBCommander.get_theme_content(theme)
    print(course_lessons)
    for lesson in course_lessons:
        course_lessons_buttons.append(InlineKeyboardButton(text = lesson[0], callback_data=lesson[1]))

    course_lessons_buttons.append(InlineKeyboardButton(text = "Վերադարձ", callback_data='back'))
    course_lessons_keyboard = InlineKeyboardMarkup(row_width=1)
    for button in course_lessons_buttons:
        course_lessons_keyboard.add(button)


    return course_lessons_keyboard
