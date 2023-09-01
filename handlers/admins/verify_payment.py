from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from loader import dp
from states.verify_payment import VerifyPayment
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from utils.db_api.models import DBCommander
from keyboards.default import disable_user_markup
from keyboards.inline import payment_requests_list_keyboard
from datetime import datetime


@dp.message_handler(Text("Հաստատել վճարումը"), state=None)
async def enter_activating_username(message: Message):
    if await DBCommander.check_if_admin(message.from_user.id) and await DBCommander.get_payment_check_requests():
        await message.answer(text="Ընտրեք օգտատիրոջը", reply_markup=await payment_requests_list_keyboard())
        await VerifyPayment.GetPaymentCheckRequests.set()

    else:
        await message.answer(text="Վճարման հաստատման հարցումներ չկան")

@dp.callback_query_handler(state=VerifyPayment.GetPaymentCheckRequests)
async def search_user(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    search_result = await DBCommander.get_payment_check_requests()
    user_id = call.data
    print(search_result)
    if search_result:
        await state.update_data(user_id=user_id)
        await call.message.answer(text=f"Հաստատել օգտատիրոջ վճարումը?", reply_markup=disable_user_markup)
    await VerifyPayment.VerifyPayment.set()

@dp.message_handler(state=VerifyPayment.VerifyPayment)
async def disable_user(message: Message, state: FSMContext):
    if await DBCommander.check_if_admin(message.from_user.id):
        if message.text == "Այո":
            data = await state.get_data()
            user_id = data.get("user_id")
            current_datetime = datetime.now()
            return_status = await DBCommander.verify_payment(int(user_id), current_datetime)
            if return_status:
                await message.answer(text=f"Վճարումը հաստատված է", reply_markup=ReplyKeyboardRemove())
                await dp.bot.send_message(user_id, "Ձեր վճարումը հաստատված է")
            await state.finish()
        elif message.text == "Ոչ":
            await message.answer(text=f"Օգտատիրոջ վճարման հաստատումը չեղարկվեց", reply_markup=ReplyKeyboardRemove())
            await state.finish()

        else:
            await message.answer(text="Անթույլատրելի գործողություն")        