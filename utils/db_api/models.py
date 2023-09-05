from aiogram import types, Bot
from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import (Column, Integer, BigInteger, String,
                        Sequence, TIMESTAMP, Boolean, JSON, Text)
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy import sql
from sqlalchemy import select

host="127.0.0.1"
user="telebot"
password="Night@Witches!#@"
database="telebot"

db = Gino()


class User(db.Model):
    __tablename__ = 'users'

    student_id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    full_name = Column(String(100))
    username = Column(String(50))
    last_payment_date = Column(TIMESTAMP)
    is_admin = Column(Boolean)
    is_active = Column(Boolean)
    current_lesson = Column(String(100))
    active_courses = Column(JSONB)
    payment_check_request = Column(Boolean)
    is_superadmin = Column(Boolean)
    homework_check_request = Column(Boolean)
    homework_content = Column(Text)
    payment_proof_path = Column(String(100))
    query: sql.Select

    def __repr__(self):
        return "<User(id='{}', fullname='{}', username='{}')>".format(
            self.student_id, self.full_name, self.username)



class Content(db.Model):
    __tablename__ = 'content'

    lesson_id = Column(Integer, primary_key=True, autoincrement=True)
    lesson_course = Column(String(100))
    lesson_name = Column(String(100))
    lesson_content = Column(String(100))
    lesson_theme = Column(String(100))
    query: sql.Select



class DBCommands:

    async def get_user(self, student_id: int):
        user = await User.query.where((User.student_id==int(student_id)) & (User.is_admin == False)).gino.first()
        return user
    
    async def get_admin(self, student_id: int):
        user = await User.query.where((User.student_id==int(student_id)) & (User.is_admin == True)).gino.first()
        return user


    async def check_if_admin(self, student_id):
        check =  await User.query.where((User.student_id == student_id) & (User.is_admin == True)).gino.first()
        if check:
            return check
        
        else:
            return False
        
    
    async def check_if_superadmin(self, student_id):
        check =  await User.query.where((User.student_id == student_id) & (User.is_superadmin == True)).gino.first()
        if check:
            return check
        
        else:
            return False
    
    async def get_non_admin_users(self):
        non_admin_users = await User.select('student_id', 'full_name').where(User.is_admin == False).gino.all()
        return non_admin_users

    async def get_user_data(self, user_id):
        user_data = await User.select('username', 'full_name').where(User.student_id == user_id).gino.all()
        return user_data
    
    async def get_admin_users(self):
        non_admin_users = await User.select('student_id').where(User.is_admin == True).gino.all()
        return non_admin_users
    
    async def get_admin_users_fork(self):
        admin_users = await User.select('student_id', 'full_name').where(User.is_admin == True).gino.all()
        return admin_users


    async def get_payment_check_requests(self):
        user = await User.select('student_id', 'full_name', 'payment_proof_path').where((User.payment_check_request == True) & (User.is_admin == False) & (User.is_superadmin == False)).gino.all()
        if user:
            return user
        return False
    
    async def get_homework_approve_requests(self):
        homework = await User.select('student_id', 'full_name', 'homework_content').where((User.homework_check_request == True) & (User.is_admin == False) & (User.is_superadmin == False)).gino.all()
        if homework:
            return homework

        return 
        
    async def get_homework_content(self, user_id):
        homework = await User.select('homework_content').where(User.student_id == user_id).gino.all() 
        return homework

    async def verify_payment(self, user_id, payment_date):

        activate_user = await User.update.values(
            is_active = True,
            current_lesson = 'Աշակերտություն',
            last_payment_date = payment_date,
            payment_check_request=False
            ).where(User.student_id == user_id).gino.status()
        
        user = await User.select('full_name').where(User.student_id==int(user_id)).gino.first()

        if activate_user:
            return user
        return False


    async def check_user_activation_status(self, user_id):
        status = await User.select('is_active').where(User.student_id == user_id).gino.scalar()
        if status:
            return True
        return False

    async def disable_user(self, user_id:int):
        user = await User.update.values(is_active=False).where(User.student_id == user_id).gino.status()
        return user
    
    async def save_homework(self, user_id:int, homework_content:str):
        save = await User.update.values(homework_check_request=True, homework_content=homework_content).where(User.student_id == user_id).gino.status()
        return save
    
    async def get_user_current_theme(self, user_id):
        current_lesson = await User.select('current_lesson').where(User.student_id == user_id).gino.first()
        return current_lesson
    
    async def approve_homework(self, user_id:int, next_theme):
        approve = await User.update.values(homework_check_request=False, homework_content="", current_lesson=next_theme).where(User.student_id == user_id).gino.status()
        return approve

    async def no_approve_homework(self, user_id:int):
        approve = await User.update.values(homework_check_request=False, homework_content="").where(User.student_id == user_id).gino.status()
        return approve
    
    async def enable_user(self, user_id:int):
        user = await User.update.values(is_active=True).where(User.student_id == user_id).gino.status()
        return user

    async def add_admin(self, user_id:int):
        user = await User.update.values(is_admin=True, is_active=True).where(User.student_id == user_id).gino.status()
        return user
    
    async def remove_admin(self, user_id:int):
        user = await User.update.values(is_admin=False).where(User.student_id == user_id).gino.status()
        return user
        
    async def send_payment_request(self, user_id:int, payment_proof_path):
        user = await User.update.values(payment_check_request=True, payment_proof_path=payment_proof_path).where(User.student_id == user_id).gino.status()
        return user
    
    async def add_content(self, lesson_course, lesson_theme, lesson_name, lesson_content):
        content = await Content.create(lesson_course=lesson_course, lesson_theme=lesson_theme, lesson_name=lesson_name, lesson_content=lesson_content)
        return content


    async def register_user(self, user_data):
        pass

    async def get_courses(self):
        unique_courses = []
        courses = await Content.select('lesson_course').gino.all()
        for course in courses:
            if str(course[0]) not in unique_courses:
                   unique_courses.append(str(course[0]))
        print(unique_courses)

        return unique_courses

    
    async def get_course_themes(self, course):
        content = await Content.select('lesson_theme').where(Content.lesson_course == course).order_by(Content.lesson_id).gino.all()
        return content

    async def get_course_unique_themes(self, course="Հայտնություն"):
        unique_themes = []
        # content = await Content.select('lesson_theme').where(Content.lesson_course == course).order_by(Content.lesson_id.asc())
        content = await Content.select("lesson_theme").where(Content.lesson_course == course).order_by(Content.lesson_id).gino.all()
        for theme in content:
            if str(theme[0]) not in unique_themes:
                unique_themes.append(str(theme[0]))

        return unique_themes
    
    async def get_theme_content(self, theme):
        content = await Content.select('lesson_name', 'lesson_id').where(Content.lesson_theme == theme).order_by(Content.lesson_id).gino.all()
        return content
    
    async def get_lesson_content(self, lesson_id):
        content = await Content.select('lesson_content').where(Content.lesson_id == lesson_id).gino.all()
        return content
    
    async def check_user_access(self, user_id, course):
        try:
            user_status = await User.select('active_courses').where(User.student_id == user_id).gino.status()
            for user_course in user_status[1][0]:
                if user_course == course:
                    return True
            return False
        except IndexError:
            return False
        
    async def add_user_to_db(self, user_id, username, fullname, payment_request, payment_proof_path="none"):
        creation_status = await User.create(student_id = user_id, full_name = fullname, username=username, is_admin=False, is_active=False, active_courses="Հայտնություն", payment_check_request=payment_request, is_superadmin=False, payment_proof_path = payment_proof_path)
        return creation_status
    
DBCommander = DBCommands()


async def create_db():
    await db.set_bind(f'postgresql://{user}:{password}@{host}/{database}')

    db.gino: GinoSchemaVisitor




