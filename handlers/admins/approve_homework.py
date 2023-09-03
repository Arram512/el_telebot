from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from loader import dp
from states.homework_approve import ApproveHomework
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from utils.db_api.models import DBCommander
from keyboards.default import disable_user_markup
from keyboards.inline import homework_approve_requests_keyboard
from datetime import datetime


@dp.message_handler(Text("Հաստատել տնային աշխատանքը"), state=None)
async def enter_activating_username(message: Message):
    if await DBCommander.check_if_admin(message.from_user.id) and await DBCommander.get_homework_approve_requests():
        await message.answer(text="Ընտրեք օգտատիրոջը", reply_markup=await homework_approve_requests_keyboard())
        await ApproveHomework.GetHomeworkApproveRequests.set()

    else:
        await message.answer(text="Ստուգման ենթակա տնային աշխատանքներ չկան")

@dp.callback_query_handler(state=ApproveHomework.GetHomeworkApproveRequests)
async def search_user(call:CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    user_id = int(call.data)
    search_result = await DBCommander.get_homework_content(user_id)
    print(search_result)
    if search_result:
        await state.update_data(user_id=user_id)
        await call.message.answer(text=f"{search_result[0][0]}")
        await call.message.answer(text=f"Հաստատել օգտատիրոջ աշխատանքը?", reply_markup=disable_user_markup)
    await ApproveHomework.ApproveHomework.set()

@dp.message_handler(Text("Այո"), state=ApproveHomework.ApproveHomework)
async def approve_homework(message: Message, state: FSMContext):
    if await DBCommander.check_if_admin(message.from_user.id):
        if message.text == "Այո":
            data = await state.get_data()
            user_id = data.get("user_id")
            all_themes = await DBCommander.get_course_unique_themes()
            current = await DBCommander.get_user_current_theme(user_id)
            current = current[0]
            current_index = all_themes.index(current)
            if current_index != all_themes[-1]:
                next_index = current_index + 1

                return_status = await DBCommander.approve_homework(int(user_id),next_theme= all_themes[next_index])

                if return_status:
                    await message.answer(text=f"Աշխատանքը հաստատված է։ Օգտատերը անցավ {all_themes[next_index]} թեմային", reply_markup=ReplyKeyboardRemove())
                    await dp.bot.send_message(user_id, f"✅Ձեր աշխատանքը հաստատված է, {all_themes[next_index]} թեման ակտիվացված է")
                await state.finish()

        else:
            await message.answer(text="Անթույլատրելի գործողություն")   

@dp.message_handler(Text("Ոչ"), state=ApproveHomework.ApproveHomework)
async def  cancel_homework(message: Message, state: FSMContext):

    await message.answer(text=f"Աշխատանքը հաստատված չէ, խնդրում ենք նկարագրել պատճառները", reply_markup=ReplyKeyboardRemove())
    await ApproveHomework.CancellationExplanations.set()

@dp.message_handler(state=ApproveHomework.CancellationExplanations)
async def  cancellation_explanations(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    await message.answer(text=f"Հիմքերը ուղարկված էն օգտատիրոջը", reply_markup=ReplyKeyboardRemove())
    await dp.bot.send_message(user_id, f"Ձեր աշխատանքը հաստատված չէ, պատճառները ներկայացված էն ստորև")
    await dp.bot.send_message(user_id, f"{message.text}")
    await DBCommander.no_approve_homework(int(user_id))
    await state.finish()