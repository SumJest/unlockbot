import typing
import requests
import aiohttp
from utils.objects import *
from utils.models import Vote, Choice, Question, Registration, Promocode, Option


class UnlockAPI:
    url = ''

    def __init__(self, url: str):
        self.url = url

    async def _get(self, function: str, params=None):
        if params is None:
            params = {}
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
            async with session.get(
                    self.url + function, params=params) as resp:
                data = await resp.text()
        return json.loads(data)

    async def getUserById(self, id: int):
        data = await self._get("participant", {"id": id})

        return objects.getUserByJson(data)

    async def getScore(self, id: int):
        data = await self._get("score", {"id": id})
        return data['data']['score']

    async def sendRegistrationData(self, username: str, deeplink: str):
        data = await self._get("/bot/id", {"username": username if username is not None else "", "deeplink": deeplink})
        return data

    async def sendVoteChoice(self, id: int, vote_id: int, choice: str):
        pass

    async def sendAnswer(self, id: int, question_id, answer: str):
        pass


    async def update_db(self):
        data = await self._get("bot/functions")
        Registration.delete().execute()
        Option.delete().execute()
        Promocode.delete().execute()
        Question.delete().execute()
        Vote.delete().execute()
        Choice.delete().execute()
        for function in data["data"]:
            match function["TYPE"]:
                case 1:  # promocode
                    promocode_model = Promocode.create(**function)
                    promocode_model.save()
                case 2:  # Question
                    question_mode = Question.create(**function)
                    question_mode.save()
                case 3:  # Vote
                    vote_model = Vote.create(**function)
                    vote_model.save()
                    for choice in function['choices']:
                        choice_model = Choice.create(vote=vote_model, name=choice)
                        choice_model.save()
                case 4:  # Registration
                    registration_model = Registration.create(**function)
                    registration_model.save()
                    for option in function['options']:
                        option_model = Option.create(**option, registration=registration_model)
                        option_model.save()
