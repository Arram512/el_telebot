from aiogram.dispatcher.filters.state import StatesGroup, State

class EnableUserGroup(StatesGroup):
    EnterUsername = State()
    UserPresenceCheck = State()
    EnableUser = State()