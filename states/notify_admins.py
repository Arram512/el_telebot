from aiogram.dispatcher.filters.state import StatesGroup, State

class NotifyAdmins(StatesGroup):
    SendNotification = State()