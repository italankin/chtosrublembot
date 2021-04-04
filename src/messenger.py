import json
import random


class Messenger:
    _usd_down: list[str]
    _rub_down: list[str]
    _neutral: list[str]

    def __init__(self, messages):
        with open(messages) as f:
            j = json.load(f)
            self._usd_down = j['usd_down']
            self._rub_down = j['rub_down']
            self._neutral = j['neutral']

    def usd_down(self) -> str:
        return random.choice(self._usd_down)

    def rub_down(self) -> str:
        return random.choice(self._rub_down)

    def neutral(self) -> str:
        return random.choice(self._neutral)
