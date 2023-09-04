from aiogram.dispatcher.filters.state import StatesGroup, State

class SubscribeToCourse(StatesGroup):
    GetUserData = State()
    PayOrLater = State()
    IfPaySendPhoto = State()
    End = State()


class SendPayment(StatesGroup):
    GetUserData = State()
    PayOrLater = State()
    IfPaySendPhoto = State()
    End = State()