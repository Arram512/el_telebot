from aiogram import types, Bot
from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import (Column, Integer, BigInteger, String,
                        Sequence, TIMESTAMP, Boolean, JSON)
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
    active_courses = Column(JSON)
    payment_check_request = Column(Boolean)
    is_superadmin = Column(Boolean)

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


    async def check_if_admin(self, student_id):
        check =  await User.query.where((User.student_id == student_id) & (User.is_admin == True)).gino.first()
        if check:
            return check
        
        else:
            return False
    
    async def get_non_admin_users(self):
        non_admin_users = await User.select('student_id', 'full_name').where(User.is_admin == False).gino.all()
        return non_admin_users
    
    async def get_payment_check_requests(self):
        user = await User.select('student_id', 'full_name').where((User.payment_check_request == True) & (User.is_admin == False) & (User.is_superadmin == False)).gino.all()
        if user:
            return user
        return False

    async def verify_payment(self, user_id, payment_date):

        activate_user = await User.update.values(
            is_active = True,
            last_payment_date = payment_date,
            payment_check_request=False
            ).where(User.student_id == user_id).gino.status()
        
        user = await User.select('full_name').where(User.student_id==int(user_id)).gino.first()
        print(user, "11111111111111111111111111111111111111111111111111")

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
    
    async def enable_user(self, user_id:int):
        user = await User.update.values(is_active=True).where(User.student_id == user_id).gino.status()
        return user
    
    async def register_user(self, user_data):
        pass

    async def get_course_themes(self, course):
        content = await Content.select('lesson_theme').where(Content.lesson_course == course).gino.all()
        return content
    
    async def get_theme_content(self, theme):
        content = await Content.select('lesson_name', 'lesson_id').where(Content.lesson_theme == theme).gino.all()
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

DBCommander = DBCommands()


async def create_db():
    await db.set_bind(f'postgresql://{user}:{password}@{host}/{database}')

    db.gino: GinoSchemaVisitor