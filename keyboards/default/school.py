from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


lessons_db = ["Գրանցվել դասընթացին ", "Թեմա 1", "Թեմա 2", "Թեմա 3", "Թեմա 4", "Թեմա 5" ]
keyboard = [[]]

for lesson in lessons_db:
    keyboard[0].append(KeyboardButton(text=lesson))

school = ReplyKeyboardMarkup(
    keyboard = keyboard,
    resize_keyboard=False
)