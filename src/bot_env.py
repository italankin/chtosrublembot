import os


class BotEnv:
    bot_token: str
    triggers_file: str
    fcs_access_key: str
    substring_trigger_rate: float

    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.triggers_file = os.getenv('BOT_TRIGGERS_FILE')
        self.fcs_access_key = os.getenv('FCSAPI_ACCESS_KEY')
        self.substring_trigger_rate = float(os.getenv('BOT_SUBSTRING_TRIGGER_RATE', '0.23'))
