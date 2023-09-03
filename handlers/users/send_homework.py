from loader import dp
from aiogram import types

from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from keyboards.default import course_themes, lesson_content
from keyboards.default.subscribe import subscribe_markup
from keyboards.default import cancel_markup
from aiogram.dispatcher.filters import Command, Text
from utils.db_api.models import DBCommander
from states.select_course import GetCourseGroup
from utils.notify_admins import notify_admins
from aiogram.dispatcher import FSMContext



@dp.callback_query_handler(lambda call: call.data == 'send_homework', state=GetCourseGroup.SelectLesson)
async def send_homework(call: CallbackQuery, state: FSMContext):
    all_themes = await DBCommander.get_course_unique_themes()
    current_theme = await DBCommander.get_user_current_theme(user_id=int(call.from_user.id))
    current_theme = current_theme[0]
    await call.answer(cache_time=60)
    data = await state.get_data()
    lesson_theme = data.get("lesson_theme")
    if all_themes.index(current_theme) == all_themes.index(lesson_theme):
        await call.message.answer(f"Ուղարկեք {lesson_theme} թեմայի տնային աշխատանքը", reply_markup=cancel_markup)
        await state.set_state(GetCourseGroup.SendHomework)
    else:
        await call.message.answer(f"{lesson_theme} թեմայի տնային աշխատանքը արդեն հաստատված է", reply_markup=ReplyKeyboardRemove())
        await call.message.answer("Ընտրեք թեման", reply_markup=await course_themes("Հայտնություն"))
        await state.set_state(GetCourseGroup.SelectTheme)


@dp.message_handler(Text("Չեղարկել❌"), state=GetCourseGroup.SendHomework)
async def cancel_sending(message: types.Message, state: FSMContext):
    await message.answer(".", reply_markup=ReplyKeyboardRemove())
    await message.answer("Ընտրեք թեման", reply_markup=await course_themes("Հայտնություն"))
    await state.set_state(GetCourseGroup.SelectTheme)


@dp.message_handler(content_types=[types.ContentType.TEXT, types.ContentType.DOCUMENT, types.ContentType.PHOTO, types.ContentType.VIDEO], state=GetCourseGroup.SendHomework)
async def handle_homework(message: types.Message, state: FSMContext):

    data = await state.get_data()
    lesson_theme = data.get("lesson_theme")
    sender_id = data.get("sender_id")

    message_text = message.text if message.text else None
    file_id = message.document.file_id if message.document else None
    photo_id = message.photo[-1].file_id if message.photo else None
    video_id = message.video.file_id if message.video else None

    themes = await DBCommander.get_course_unique_themes()
    sender = await DBCommander.get_user_data(sender_id)

    if message_text:

        save = await DBCommander.save_homework(sender_id, str(message_text))
        if save:
            await message.answer(f"🔁Ձեր աշխատանքը ուղարկված է, սպասեք հաստատման")
            await notify_admins(dp=dp, user_data=sender , action = "Տնային աշխատանքի նոր հաստատման հայտ")
            await message.answer("Ընտրեք թեման", reply_markup=await course_themes("Հայտնություն"))
            
            await state.set_state(GetCourseGroup.SelectTheme)

    else:
        await message.answer("Ուղարկեք որպես նամակ")
