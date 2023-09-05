from aiogram.dispatcher.filters.state import StatesGroup, State

class NotifyAll(StatesGroup):
    SendNotification = State()