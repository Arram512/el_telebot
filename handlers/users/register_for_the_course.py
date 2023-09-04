from loader import dp
from aiogram.types import Message, ContentType
from keyboards.default import school
from keyboards.default.menu import menu_for_users
from aiogram.dispatcher.filters import Command, Text
from states.subscribe_to_course import SubscribeToCourse
from aiogram.dispatcher import FSMContext
import keyboards.default.disable_user as choice_markup
from utils.db_api.models import DBCommander
import os



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

    await message.answer("Ուղարկեք փոխանցումը հավաստող կտրոնը")
    await SubscribeToCourse.IfPaySendPhoto.set()

@dp.message_handler(content_types=ContentType.PHOTO, state = SubscribeToCourse.IfPaySendPhoto)
async def handle_photo(message: Message, state: FSMContext):
    print("hitler_alert")
    photo_folder = "C:\\Users\\User\\Desktop\\aiogram-bible"
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
    await DBCommander.add_user_to_db(user_id=user_id, username=username, fullname=fullname, payment_request=payment_request, payment_proof_path=str(photo_path))
    await message.answer("Շնորհակալություն գրանցման համար։ Ձեր հայտը կհաստատվի ադմինիստրատորի կողմից դիտարկվելուց հետո", reply_markup=menu_for_users)
    await state.finish()


@dp.message_handler(Text(choice_markup.no), state = SubscribeToCourse.PayOrLater)
async def register_without_payment(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    username = data.get("username")
    fullname = data.get("fullname")
    payment_request = False
    await DBCommander.add_user_to_db(user_id=user_id, username=username, fullname=fullname, payment_request=payment_request)
    await state.finish()
    await message.answer("Գրանցումը ավարտվեց", reply_markup=menu_for_users)




    

