from typing import Optional

from telegram import Update, ChatAction
from telegram.ext import Dispatcher, MessageHandler, Filters, CallbackContext

from bot_context import incontext, BotContext


def register(dispatcher: Dispatcher):
    filters = Filters.text & (~Filters.command) & (~Filters.forwarded) & (~Filters.caption)
    dispatcher.add_handler(MessageHandler(filters, _command, run_async=True))


@incontext
def _command(bot_context: BotContext, update: Update, _):
    if not update.message:
        return
    text = update.message.text
    symbol = _find_symbol(bot_context, text)
    if not symbol:
        return
    update.message.reply_chat_action(ChatAction.TYPING)
    status = bot_context.chtosrublem.status(symbol)
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


def _find_symbol(bot_context: BotContext, text: str) -> Optional[str]:
    for pattern, symbol in bot_context.triggers:
        if pattern.fullmatch(text):
            return symbol
    return None
