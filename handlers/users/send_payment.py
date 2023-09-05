from loader import dp
from aiogram.types import Message
from keyboards.default import menu_for_users
from keyboards.default import menu_for_admins
from aiogram.dispatcher.filters import Command, Text
from utils.db_api.models import DBCommander
from states.subscribe_to_course import SendPayment
import keyboards.default.disable_user as choice_markup
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
import os


@dp.message_handler(Command("send_payment"), state=None)
async def save_user_data(message: Message, state: FSMContext):

    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    fullname = f"{first_name} {last_name}"
    await state.update_data(user_id=user_id, username=username, fullname=fullname)

    await message.answer(f"{username}\n{first_name}\n{last_name}\n\n Ուղարկել վճարման ստուգման հայտ?", reply_markup=choice_markup.disable_user_markup)
    await SendPayment.PayOrLater.set()

@dp.message_handler(Text(choice_markup.yes), state = SendPayment.PayOrLater)
async def send_payment_check_request(message: Message, state: FSMContext):

    await message.answer("Ուղարկեք փոխանցումը հավաստող կտրոնը")
    await SendPayment.IfPaySendPhoto.set()


@dp.message_handler(Text("Չեղարկել"), state = SendPayment.PayOrLater)
async def cancel(message: Message, state: FSMContext):

    await message.answer("Չեղարկված է")
    await state.finish()




@dp.message_handler(content_types=ContentType.PHOTO, state = SendPayment.IfPaySendPhoto)
async def handle_photo(message: Message, state: FSMContext):
    photo_folder = "/home/telegram/el_telebot/checks"
    if not os.path.exists(photo_folder):
        os.makedirs(photo_folder)
    
    user_id = message.from_user.id
    date = message.date.strftime('%Y-%m-%d_%H-%M-%S')
    
    unique_filename = f'{user_id}_{date}.jpg'
    
    photo_path = os.path.join(photo_folder, unique_filename)

    data = await state.get_data()
    user_id = data.get("user_id")
    username = data.get("username")
    fullname = data.get("fullname")
    payment_request = True
    
    await message.photo[-1].download(photo_path)
    await DBCommander.send_payment_request(user_id=user_id, payment_proof_path=str(photo_path))
    await message.answer("Շնորհակալություն վճարման համար։ Ձեր հայտը կհաստատվի ադմինիստրատորի կողմից դիտարկվելուց հետո", reply_markup=menu_for_users)
    await state.finish()


@dp.message_handler(Text(choice_markup.no), state = SendPayment.PayOrLater)
async def register_without_payment(message: Message, state: FSMContext):

    await state.finish()
    await message.answer("Վճարումը չեղարկվեց", reply_markup=menu_for_users)
