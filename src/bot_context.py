import json
import re
from functools import wraps

from message_trigger import MessageTrigger
from bot_env import BotEnv
from chtosrublem import ChtoSRublem
from messengers.noop import NoOpMessenger
from rates.fcsapi import FcsApi
from rates.get_rate import GetRate


class BotContext:
    bot_env: BotEnv
    get_rate: GetRate
    chtosrublem: ChtoSRublem
    triggers: list[MessageTrigger]

    def __init__(self):
        self.bot_env = BotEnv()
        self.triggers = self._parse_triggers()
        self.get_rate = FcsApi(self.bot_env.fcs_access_key, [t.symbol for t in self.triggers])
        self.chtosrublem = ChtoSRublem(self.get_rate, NoOpMessenger())

    def _parse_triggers(self) -> list[MessageTrigger]:
        if not self.bot_env.triggers_file:
            raise ValueError(f"Triggers file is not set")
        with open(self.bot_env.triggers_file) as f:
            root = json.load(f)
            return [BotContext._parse_node(node) for node in root]

    @staticmethod
    def _parse_node(node) -> MessageTrigger:
        substring = re.compile(node['substring']) if 'substring' in node else None
        captions = node.get('captions', [])
        fullmatch = re.compile(node['trigger'], flags=re.IGNORECASE)
        return MessageTrigger(fullmatch, substring, node['symbol'], captions)

    @staticmethod
    def _get_messenger_data(triggers: list[MessageTrigger]) -> dict[str, list[str]]:
        messenger_data = {}
        for trigger in triggers:
            if len(trigger.captions) == 0:
                continue
            messenger_data[trigger.symbol] = trigger.captions
        return messenger_data

    @staticmethod
    def get() -> 'BotContext':
        return _bot_context


def incontext(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        return func(BotContext.get(), update, context, *args, **kwargs)

    return wrapped


_bot_context = BotContext()
