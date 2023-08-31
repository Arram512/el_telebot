from aiogram.dispatcher.filters.state import StatesGroup, State

class SubscribeToCourse(StatesGroup):
    GetUserData = State()
    PayOrLater = State()
    End = State()
