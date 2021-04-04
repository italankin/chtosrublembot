from functools import wraps

from bot_env import BotEnv
from messenger import Messenger
from chtosrublem import ChtoSRublem
from rates.tinkoff_invest import TinkoffInvest
from rates.usd_rub_rate import UsdRubRate


class BotContext:
    bot_env: BotEnv
    usd_rub_rate: UsdRubRate
    messenger: Messenger
    chtosrublem: ChtoSRublem

    def __init__(self):
        self.bot_env = BotEnv()
        self.usd_rub_rate = TinkoffInvest(
            self.bot_env.tinkoff_invest_api_token,
            self.bot_env.tinkoff_invest_api_base_url
        )
        self.messenger = Messenger(self.bot_env.responses_file)
        self.chtosrublem = ChtoSRublem(self.usd_rub_rate, self.messenger)

    @staticmethod
    def get() -> 'BotContext':
        return _bot_context


def incontext(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        return func(BotContext.get(), update, context, *args, **kwargs)

    return wrapped


_bot_context = BotContext()
