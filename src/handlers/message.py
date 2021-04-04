from telegram import Update
from telegram.ext import Dispatcher, MessageHandler, Filters, CallbackContext

from bot_context import incontext, BotContext


def register(dispatcher: Dispatcher):
    filters = Filters.text & (~Filters.command) & (~Filters.forwarded) & (~Filters.caption)
    dispatcher.add_handler(MessageHandler(filters, _command, run_async=True))


@incontext
def _command(bot_context: BotContext, update: Update, context: CallbackContext):
    text = update.message.text
    if not _is_trigger(bot_context, context, text):
        return
    status = bot_context.chtosrublem.status()
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


def _is_trigger(bot_context: BotContext, context: CallbackContext, text: str) -> bool:
    s = text.lower()
    if s == f"@{context.bot.username}":
        return True
    return bot_context.bot_env.trigger_pattern.fullmatch(s) is not None
