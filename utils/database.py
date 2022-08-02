import sqlite3
import typing

from sqlite3 import Connection
from utils import config
from utils.objects import *

sqlite_connection = sqlite3.connect(config.getDatabasePath())


def del_participant(id: int):
    cursor = sqlite_connection.cursor()
    cursor.execute(f"delete from participant where chat_id={id}")
    cursor.close()
    sqlite_connection.commit()


def get_participant(id: int) -> User:
    cursor = sqlite_connection.cursor()
    cursor.execute(f"SELECT * FROM participants WHERE chat_id={id}")

    result = cursor.fetchall()
    if not result:
        return None
    return User(*result[0])


def get_participants() -> typing.List[User]:
    cursor = sqlite_connection.cursor()
    cursor.execute(f"SELECT * FROM participants")
    result = cursor.fetchall()
    if not result:
        return None
    return [User(*user) for user in result]


def save_user(user: User):
    cursor = sqlite_connection.cursor()
    cursor.execute(f"INSERT or REPLACE INTO participants VALUES{str(user)}")
    sqlite_connection.commit()
    cursor.close()


def is_admin(id: int):
    cursor = sqlite_connection.cursor()
    cursor.execute(f"SELECT is_admin FROM participants WHERE chat_id={id}")

    result = cursor.fetchall()
    if not result:
        return None
    return result[0][0]


def get_admins() -> typing.List[User]:
    cursor = sqlite_connection.cursor()
    cursor.execute(f"SELECT * FROM participants WHERE is_admin=1")
    result = cursor.fetchall()
    if not result:
        return None
    return [User(*i) for i in result]

def save_votes(votes: typing.List[APIVote]):

    pass

def save_questions():
    pass

def save_promocodes():
    pass

def save_registrations():
    pass

def close():
    sqlite_connection.close()
