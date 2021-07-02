import os


class BotEnv:
    bot_token: str
    triggers_file: str
    responses_file: str

    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.triggers_file = os.getenv('BOT_TRIGGERS_FILE')
