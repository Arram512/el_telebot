from loader import dp
from aiogram.types import Message, CallbackQuery
from keyboards.default import course_themes, lesson_content
from aiogram.dispatcher.filters import Command, Text
from utils.db_api.models import DBCommander
from states.select_course import GetCourseGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


@dp.message_handler(Text("Հայտնության դպրոց"), state=None)
async def get_selected_module(message: Message, state: FSMContext):
    if await DBCommander.check_user_access(message.from_id, 'Հայտնություն'):
        await message.answer(f"Անցում հայտնության դպրոց", reply_markup=await course_themes("Հայտնություն"))
        
        await GetCourseGroup.SelectTheme.set()
    else:
        await message.answer("Դուք գրանցված չեք դասընթացին, սեղմեք կոճակը գրանցվելու համար")


@dp.callback_query_handler(state=GetCourseGroup.SelectTheme)
async def get_theme_content(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    if call.data == "back":
        await state.finish()
    else:
        lesson_theme = call.data
        await call.message.answer(text=f"Ընտրեք դասը", reply_markup=await lesson_content(lesson_theme))
        await GetCourseGroup.SelectLesson.set()


@dp.callback_query_handler(state=GetCourseGroup.SelectLesson)
async def get_lesson_content(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)


    if call.data == 'back':
        await GetCourseGroup.SelectTheme.set()
    
    if await DBCommander.check_user_activation_status(int(call.from_user.id)):
        lesson_id = call.data
        get_lesson_content = await DBCommander.get_lesson_content(int(lesson_id))
        print(get_lesson_content)
        if get_lesson_content:
            await call.message.answer(text=f"{get_lesson_content[0][0]}")
            await GetCourseGroup.SelectLesson.set()
        await GetCourseGroup.SelectLesson.set()
    
    else:
        await call.message.answer(text=f"Դուք ապաակտիվացված եք, դրա համար չեք կարող դիտել դասը, մուծեք փողերը որ լավ ըլնի😄")
        await GetCourseGroup.SelectLesson.set()



