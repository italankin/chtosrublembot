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

    def usd_down(self, price: float) -> str:
        s = random.choice(self._usd_down)
        return self._with_price(s, price)

    def rub_down(self, price: float) -> str:
        s = random.choice(self._rub_down)
        return self._with_price(s, price)

    def neutral(self) -> str:
        return random.choice(self._neutral)

    def _with_price(self, s: str, price: float) -> str:
        if '%v' in s:
            return s.replace('%v', str(price))
        else:
            return s
