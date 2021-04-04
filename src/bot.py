import logging
import os
from handlers import message

from bot_context import BotContext
from telegram.ext import Updater

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG if os.getenv('DEBUG') == "1" else logging.WARNING
)

matplotlib_logger = logging.getLogger('matplotlib')
matplotlib_logger.setLevel(logging.WARNING)

updater = Updater(token=BotContext.get().bot_env.bot_token, workers=4)
dispatcher = updater.dispatcher

message.register(dispatcher)

updater.start_polling()
updater.idle()
