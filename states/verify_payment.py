from aiogram.dispatcher.filters.state import StatesGroup, State

class VerifyPayment(StatesGroup):
    GetPaymentCheckRequests = State()
    VerifyPayment = State()