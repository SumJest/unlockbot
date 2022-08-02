import json

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from utils import database as db


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        chat_id = message.chat.id
        is_admin = db.is_admin(chat_id)
        return is_admin if is_admin is not None else False


class CallbackType(BoundFilter):
    callback_type: str

    def __init__(self, callback_type: str):
        self.callback_type = callback_type

    async def check(self, callback: types.CallbackQuery) -> bool:
        try:
            data = json.loads(callback.data)
            return data['type'] == self.callback_type
        except:
            return False
