import os
import re
from typing import Optional, Pattern


class BotEnv:
    bot_token: str
    tinkoff_invest_api_token: str
    tinkoff_invest_api_base_url: str
    trigger_pattern: Pattern[str]
    responses_file: str

    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.tinkoff_invest_api_token = os.getenv('TINKOFF_INVEST_API_TOKEN')
        self.tinkoff_invest_api_base_url = os.getenv('TINKOFF_INVEST_API_BASE_URL')
        self.trigger_pattern = self._parse_trigger_messages(os.getenv('BOT_TRIGGER_PATTERN'))
        self.responses_file = os.getenv('BOT_RESPONSES_FILE')

    @staticmethod
    def _parse_trigger_messages(param: Optional[str]) -> Pattern[str]:
        if not param:
            return re.compile(".+", flags=re.RegexFlag.IGNORECASE)
        return re.compile(param, flags=re.RegexFlag.IGNORECASE)
