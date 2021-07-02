import json
import re
from functools import wraps
from typing import Pattern, Tuple

from bot_env import BotEnv
from chtosrublem import ChtoSRublem
from rates.fcsapi import FcsApi
from rates.get_rate import GetRate


class BotContext:
    bot_env: BotEnv
    get_rate: GetRate
    chtosrublem: ChtoSRublem
    triggers: list[Tuple[Pattern, str]]

    def __init__(self):
        self.bot_env = BotEnv()
        self.get_rate = FcsApi(self.bot_env.fcs_access_key)
        self.chtosrublem = ChtoSRublem(self.get_rate)
        self.triggers = self._parse_triggers()

    def _parse_triggers(self) -> list[Tuple[Pattern, str]]:
        if not self.bot_env.triggers_file:
            raise ValueError(f"Triggers file is not set")
        with open(self.bot_env.triggers_file) as f:
            root = json.load(f)
            return [(re.compile(node['trigger'], flags=re.IGNORECASE), node['symbol']) for node in root]

    @staticmethod
    def get() -> 'BotContext':
        return _bot_context


def incontext(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        return func(BotContext.get(), update, context, *args, **kwargs)

    return wrapped


_bot_context = BotContext()
