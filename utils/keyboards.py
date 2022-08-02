import json
import typing

from aiogram import types
from utils import messages
from utils.models import User


from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton


class KeyboardManager:
    def __init__(self):
        pass

    def getMainKeyboard(self, user: User):
        keyboard = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
        if user.admin_mode:
            # admin keyboard
            keyboard.add(messages.broadcast)
            keyboard.add(messages.update_db)
            keyboard.add(messages.votes)
            keyboard.add(messages.questions)
            # keyboard.add(messages.)
            keyboard.add(messages.turn_off_admin)
        else:
            keyboard.add(messages.score_request, messages.daily_report, messages.promocode)
            if user.is_admin:
                keyboard.add(messages.turn_on_admin)
        return keyboard

    def getVoteKeyboard(self, vote_id: int, choices):
        vote_keyboard = InlineKeyboardMarkup()

        for choice in choices:
            data = json.dumps({"type": "vote", "id": vote_id, "choice": choice.get_id()})
            vote_keyboard.add(InlineKeyboardButton(text=choice.name, callback_data=data))


        return vote_keyboard

    def getVotesListKeyboard(self, votes):
        votes_list = InlineKeyboardMarkup()

        for vote in votes:
            data = {"type": "vote_select", "id": vote.id}
            votes_list.add(InlineKeyboardButton(text=vote.title, callback_data=json.dumps(data)))

        data = {"type": "vote_select", "id": -1}
        votes_list.add(InlineKeyboardButton(text=messages.cancel, callback_data=json.dumps(data)))

        return votes_list

    def getQuestionsListKeyboard(self, questions):
        questions_list = InlineKeyboardMarkup()

        for question in questions:
            data = {"type": "question_select", "id": question.id}
            questions_list.add(InlineKeyboardButton(text=question.title, callback_data=json.dumps(data)))

        data = {"type": "question_select", "id": -1}
        questions_list.add(InlineKeyboardButton(text=messages.cancel, callback_data=json.dumps(data)))

        return questions_list

    def getAnswerKeyboard(self, question_id: int):
        answerkeyboard = InlineKeyboardMarkup()
        data = dict(type="answer", id=question_id)
        answerkeyboard.add(InlineKeyboardButton(text=messages.answer, callback_data=json.dumps(data)))
        return answerkeyboard

    def getCancelKeyboard(self):
        keyboard = types.reply_keyboard.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(messages.cancel)
        return keyboard
