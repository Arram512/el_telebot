
from aiogram.dispatcher.filters.state import StatesGroup, State

class AddContent(StatesGroup):

    SelectCourse = State()
    SelectTheme = State()
    AddName = State()
    AddContent = State()
