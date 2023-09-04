from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from loader import dp
from states.add_content import AddContent
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from utils.db_api.models import DBCommander
from keyboards.inline import courses_keyboard
from keyboards.default.school import course_themes

@dp.message_handler(Text("Ավելացնել կոնտենտ"), state=None)
async def add_content_step1(message: Message):
    if await DBCommander.check_if_admin(message.from_user.id):
        await message.answer(text="Ընտրեք դասընթացը", reply_markup=await courses_keyboard())
        await AddContent.SelectCourse.set()

@dp.callback_query_handler(state=AddContent.SelectCourse)
async def add_content_select_theme(call:CallbackQuery, state: FSMContext):
    
    await call.answer(cache_time=60)
    await state.update_data(course = call.data)
    
    await call.message.answer(text=f"Ընտրեք թեման", reply_markup= await course_themes(str(call.data)))
    await AddContent.SelectTheme.set()

@dp.callback_query_handler(state=AddContent.SelectTheme)
async def add_content_add_name(call:CallbackQuery, state: FSMContext):
    
    await call.answer(cache_time=60)
    await state.update_data(theme = call.data)
    
    await call.message.answer(text=f"Ուղարկեք անվանումը")
    await AddContent.AddName.set()


@dp.message_handler(state=AddContent.AddName)
async def add_content_add_url(message: Message, state: FSMContext):
    await state.update_data(content_name = str(message.text))
    await message.answer(text="Ուղարկեք url-y")
    await AddContent.AddContent.set()

@dp.message_handler(state=AddContent.AddContent)
async def add_content_add_url(message: Message, state: FSMContext):
    data = await state.get_data()
    lesson_course = data.get("course")
    lesson_theme = data.get("theme")
    lesson_name = data.get("content_name")
    lesson_content = str(message.text)
    print(lesson_course, lesson_theme, lesson_name, lesson_content)
    cont = await DBCommander.add_content(lesson_course=str(lesson_course), lesson_theme=str(lesson_theme), lesson_name=str(lesson_name), lesson_content=str(lesson_content))
    if cont:
        await message.answer(text="Ավելացված է") 
    await state.finish()