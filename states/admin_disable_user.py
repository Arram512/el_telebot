from aiogram.dispatcher.filters.state import StatesGroup, State

class DisableUserGroup(StatesGroup):
    EnterUsername = State()
    UserPresenceCheck = State()
    DisableUser = State()