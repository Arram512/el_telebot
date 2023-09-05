from aiogram.dispatcher.filters.state import StatesGroup, State

class AddAdministrator(StatesGroup):
    EnterUsername = State()
    UserPresenceCheck = State()
    AddAdmin = State()