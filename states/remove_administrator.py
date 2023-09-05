from aiogram.dispatcher.filters.state import StatesGroup, State

class RemoveAdministrator(StatesGroup):
    EnterUsername = State()
    UserPresenceCheck = State()
    RemoveAdmin = State()