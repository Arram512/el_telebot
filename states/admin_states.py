from aiogram.dispatcher.filters.state import StatesGroup, State

class AdminStates(StatesGroup):
    StartAdminAction = State()
    NotifyUsers = State()
    NotifyAdmins = State()
