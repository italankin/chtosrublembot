import random
from typing import Optional, Tuple

from telegram import Update, ChatAction
from telegram.ext import Dispatcher, MessageHandler, Filters

from bot_context import incontext, BotContext


def register(dispatcher: Dispatcher):
    filters = Filters.text & (~Filters.command)
    dispatcher.add_handler(MessageHandler(filters, _command, run_async=True))


@incontext
def _command(bot_context: BotContext, update: Update, _):
    if not update.message:
        return
    text = update.message.text
    source, symbol = _find_symbol(bot_context, text)
    if not symbol:
        return
    update.message.reply_chat_action(ChatAction.TYPING)
    status = bot_context.chtosrublem.status(source, symbol)
    if not status:
        return
    if status.plot:
        update.effective_message.reply_photo(
            photo=status.plot,
            caption=status.text,
            reply_to_message_id=update.effective_message.message_id
        )
    else:
        update.effective_message.reply_text(
            text=status.text,
            reply_to_message_id=update.effective_message.message_id
        )


def _find_symbol(bot_context: BotContext, text: str) -> Optional[Tuple[str, str]]:
    for trigger in bot_context.triggers:
        if trigger.fullmatch.fullmatch(text):
            return trigger.source, trigger.symbol
        if trigger.substring and trigger.substring.search(text):
            if random.random() <= bot_context.bot_env.substring_trigger_rate:
                return trigger.source, trigger.symbol
    return None
