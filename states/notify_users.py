from aiogram.dispatcher.filters.state import StatesGroup, State

class NotifyUsers(StatesGroup):
    EnterUsername = State()
    SendNotification = State()