import os


class BotEnv:
    bot_token: str
    triggers_file: str
    fcs_access_key: str

    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.triggers_file = os.getenv('BOT_TRIGGERS_FILE')
        self.fcs_access_key = os.getenv('FCSAPI_ACCESS_KEY')
