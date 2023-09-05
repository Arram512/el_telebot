from loader import dp
from aiogram import types
from aiogram.types import Message, CallbackQuery
from keyboards.default import course_themes, lesson_content
from keyboards.default.subscribe import subscribe_markup
from keyboards.default import disable_user_markup
from aiogram.dispatcher.filters import Command, Text
from utils.db_api.models import DBCommander
from states.select_course import GetCourseGroup
from states.subscribe_to_course import SubscribeToCourse
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import ChatNotFound


@dp.message_handler(Text("Հայտնության դպրոց"), state=None)
async def get_selected_module(message: Message, state: FSMContext):
    if await DBCommander.check_user_access(message.from_id, 'Հայտնություն'):
        await message.answer(f"Անցում հայտնության դպրոց", reply_markup=await course_themes("Հայտնություն"))
        
        await GetCourseGroup.SelectTheme.set()
    else:
        await message.answer("Դուք գրանցված չեք դասընթացին, սեղմեք կոճակը գրանցվելու համար", reply_markup=subscribe_markup)
        await SubscribeToCourse.GetUserData.set()



@dp.message_handler(Text("Հայտնության դպրոց, կուրս 2"), state=None)
async def get_selected_module(message: Message, state: FSMContext):
    if await DBCommander.check_user_access(message.from_id, 'Հայտնություն2'):
        await message.answer(f"Անցում հայտնության դպրոց", reply_markup=await course_themes("Հայտնություն2"))
        
        await GetCourseGroup.SelectTheme.set()
    else:
        await message.answer("Դուք գրանցված չեք դասընթացին, սեղմեք կոճակը գրանցվելու համար", reply_markup=subscribe_markup)
        await SubscribeToCourse.GetUserData.set()


@dp.callback_query_handler(state=GetCourseGroup.SelectTheme)
async def get_theme_content(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    if call.data == "back":
        await state.finish()
    else:
        lesson_theme = call.data
        await state.update_data(lesson_theme=lesson_theme, sender_id= call.from_user.id)
        print(lesson_theme)
        current_theme = await DBCommander.get_user_current_theme(int(call.from_user.id))
        print(current_theme)
        current_theme = current_theme[0]

        all_themes = await DBCommander.get_course_unique_themes()
        
        if all_themes.index(str(lesson_theme)) <= all_themes.index(str(current_theme)):
            print(str(current_theme))
            print(str(lesson_theme))
            await call.message.answer(text=f"Ընտրեք դասը", reply_markup=await lesson_content(lesson_theme))
            await GetCourseGroup.SelectLesson.set()

        else: 
            await call.message.answer(f"{lesson_theme} թեման ձեզ հասանելի չէ, նախ ավարտեք {current_theme} թեման", reply_markup=await course_themes("Հայտնություն"))
            await GetCourseGroup.SelectTheme.set()

@dp.callback_query_handler(lambda call: call.data == 'back', state=GetCourseGroup.SelectLesson)
async def back_to_select_theme(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.answer("Ընտրեք թեման", reply_markup=await course_themes("Հայտնություն"))
    await state.set_state(GetCourseGroup.SelectTheme)
    



@dp.callback_query_handler(state=GetCourseGroup.SelectLesson)
async def get_lesson_content(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    data = await state.get_data()
    lesson_theme = data.get("lesson_theme")
    
    if await DBCommander.check_user_activation_status(int(call.from_user.id)) or lesson_theme == "Աշակերտություն" or int(call.data) == 11:
        lesson_id = call.data
        get_lesson_content = await DBCommander.get_lesson_content(int(lesson_id))
        print(get_lesson_content)
        if get_lesson_content:
            await call.message.answer(text=f"{get_lesson_content[0][0]}")
            await GetCourseGroup.SelectLesson.set()
        await GetCourseGroup.SelectLesson.set()
        await call.message.answer(text=f"Ընտրեք դասը", reply_markup=await lesson_content(lesson_theme))
    
    else:
        await call.message.answer(text=f"Դուք ապաակտիվացված եք, դրա համար չեք կարող դիտել դասը։ Դասընթացը ամբողջությամբ դիտելու համար կատարեք վճարում և ուղարկեք ստուգման հայտ\nԴպրոցի վճարը կազմում է ամսեկան 10․000 դրամ\nԱմբողջ դպրոցի կուրսը կազմում է 60000 դր․\nՎճարման հաշվեհամարները\nUNIBANK \n24100054017903 Հաշվեհամար\n4374690100306891 Քարտի համար\nVarazdat Bekzadyan\nTelcell ID 82675528 ,  Հեռ   +37499999610\nIdram ID 410275602 , Հեռ  +37499999610")
        await state.finish()



