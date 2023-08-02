from aiogram import types, Bot
from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import (Column, Integer, BigInteger, String,
                        Sequence, TIMESTAMP, Boolean, JSON)
from sqlalchemy import sql

host="128.140.41.181"
user="telebot"
password="Night@Witches!#@"
database="el_telebot"

db = Gino()


class User(db.Model):
    __tablename__ = 'users'

    student_id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    full_name = Column(String(100))
    username = Column(String(50))
    last_payement_date = Column(TIMESTAMP)
    is_admin = Column(Boolean)
    is_active = Column(Boolean)
    current_lesson = Column(String(100))
    active_courses = Column(JSON)

    query: sql.Select

    def __repr__(self):
        return "<User(id='{}', fullname='{}', username='{}')>".format(
            self.id, self.full_name, self.username)



class Purchase(db.Model):
    __tablename__ = 'content'

    lesson_id = Column(Integer)
    lesson_course = Column(String(100))
    lesson_name = Column(String(100))
    lesson_content = Column(String(100))
    query: sql.Select



class DBCommands:

    async def get_user(self, student_username):
        print(student_username)
        print(type(student_username))
        #user = await User.query.where(User.username == student_username).gino.first()
        user = await User.query.where(User.username.ilike(f'%{student_username}%')).gino.first()

        return user

    async def check_if_admin(self, student_id):
        check =  await User.query.where((User.student_id == student_id) & (User.is_admin == True)).gino.first()
        return check is not None

DBCommander = DBCommands()


async def create_db():
    await db.set_bind(f'postgresql://{user}:{password}@{host}/{database}')

    db.gino: GinoSchemaVisitor