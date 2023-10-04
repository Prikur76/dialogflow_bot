import logging
import os

from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import (Updater, CommandHandler,
                          MessageHandler, Filters,
                          CallbackContext)

from dialog_flow import DialogFlow
from error_handler import LogsHandler

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуй, {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True))


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo_with_dialogflow(update: Update, context: CallbackContext) -> None:
    """Возвращает ответ DialogFlow."""
    session_id = update.effective_chat.id
    user_message = update.message.text
    try:
        flow = DialogFlow(os.getenv('PROJECT_ID'))
        flow_answer = flow.detect_intent_text(
            session_id, user_message)
        update.message.reply_text(flow_answer['answer'])
    except Exception:
        logger.exception('Возникла проблема с DialogFlow')


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(LogsHandler())
    logger.info('Бот запущен')

    try:
        updater = Updater(os.getenv('DF_BOT_TOKEN'))
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CommandHandler("help", help_command))
        dispatcher.add_handler(MessageHandler(
            Filters.text & ~Filters.command, echo_with_dialogflow)
        )

        updater.start_polling()
        updater.idle()
    except Exception:
        logger.exception('Возникла ошибка в боте')
