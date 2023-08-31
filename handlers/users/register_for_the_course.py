from loader import dp
from aiogram.types import Message
from keyboards.default import school
from aiogram.dispatcher.filters import Command, Text
from states.subscribe_to_course import SubscribeToCourse
from aiogram.dispatcher import FSMContext



@dp.message_handler(Text("Գրանցվել դասընթացին"), state=SubscribeToCourse.GetUserData)
async def save_user_data(message: Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    firstname = message.from_user.first_name
    lastname = message.from_user.last_name

