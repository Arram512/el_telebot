from aiogram.dispatcher.filters.state import StatesGroup, State

class GetCourseGroup(StatesGroup):
    SelectTheme = State()
    SelectLesson = State()
    SendHomework = State()
    GetHomeworkAndApprove = State()
    GetLessonContent = State()
