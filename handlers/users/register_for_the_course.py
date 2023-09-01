from loader import dp
from aiogram.types import Message
from keyboards.default import school
from keyboards.default.menu import menu_for_users
from aiogram.dispatcher.filters import Command, Text
from states.subscribe_to_course import SubscribeToCourse
from aiogram.dispatcher import FSMContext
import keyboards.default.disable_user as choice_markup
from utils.db_api.models import DBCommander



@dp.message_handler(Text("Գրանցվել դասընթացին"), state=SubscribeToCourse.GetUserData)
async def save_user_data(message: Message, state: FSMContext):

    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    fullname = f"{first_name} {last_name}"
    await state.update_data(user_id=user_id, username=username, fullname=fullname)

    await message.answer(f"{username}\n{first_name}\n{last_name}\n\n Ուղարկել վճարման ստուգման հայտ?", reply_markup=choice_markup.disable_user_markup)
    await SubscribeToCourse.PayOrLater.set()

@dp.message_handler(Text(choice_markup.yes), state = SubscribeToCourse.PayOrLater)
async def send_payment_check_request(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    username = data.get("username")
    fullname = data.get("fullname")
    payment_request = True
    await DBCommander.add_user_to_db(user_id=user_id, username=username, fullname=fullname, payment_request=payment_request)
    await state.finish()
    await message.answer("Գարանցումը ավարտվեց", reply_markup=menu_for_users)

@dp.message_handler(Text(choice_markup.yes), state = SubscribeToCourse.PayOrLater)
async def register_without_payment(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    username = data.get("username")
    fullname = data.get("fullname")
    payment_request = False
    await DBCommander.add_user_to_db(user_id=user_id, username=username, fullname=fullname, payment_request=payment_request)
    await state.finish()
    await message.answer("Գարանցումը ավարտվեց", reply_markup=menu_for_users)




    

