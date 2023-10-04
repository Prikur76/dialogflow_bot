import logging
import os

from dotenv import load_dotenv
from telegram import Update, ForceReply, Bot
from telegram.ext import (Updater, CommandHandler,
                          MessageHandler, Filters,
                          CallbackContext)

from dialog_flow import DialogFlow
from logshandler import TelegramLogsHandler

load_dotenv()

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Отправляет привественное сообщение при команде /start"""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуй, {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True))


def help_command(update: Update, context: CallbackContext) -> None:
    """Отправляет привественное сообщение при команде /help"""
    update.message.reply_text('Help!')


def echo_with_dialogflow(update: Update, context: CallbackContext) -> None:
    """Возвращает ответ DialogFlow."""
    session_id = update.effective_chat.id
    user_message = update.message.text
    flow = DialogFlow(os.environ.get('PROJECT_ID'))
    flow_answer = flow.detect_intent_text(
        session_id, user_message)
    if flow_answer:
        update.message.reply_text(flow_answer['answer'])
    return


if __name__ == '__main__':
    admin_chat_id = os.environ.get('SERVICE_CHAT_ID')
    admin_bot = Bot(token=os.environ.get('SERVICE_BOT_TOKEN'))
    admin_bot_handler = TelegramLogsHandler(
        admin_bot, admin_chat_id)
    admin_bot_handler.setLevel(logging.DEBUG)
    botformatter = logging.Formatter(
        fmt='{message}', style='{')
    admin_bot_handler.setFormatter(botformatter)
    logger.addHandler(admin_bot_handler)

    streamhandler = logging.StreamHandler()
    streamhandler.setLevel(logging.ERROR)
    streamformatter = logging.Formatter(
        fmt='{asctime} - {levelname} - {name} - {message}',
        style='{')
    streamhandler.setFormatter(streamformatter)
    logger.addHandler(streamhandler)
    logger.debug('TG бот запущен')

    try:
        updater = Updater(os.environ.get('DF_BOT_TOKEN'))
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler('start', start))
        dispatcher.add_handler(CommandHandler('help', help_command))
        dispatcher.add_handler(MessageHandler(
            Filters.text & ~Filters.command, echo_with_dialogflow)
        )

        updater.start_polling()
        updater.idle()

    except Exception as e:
        logger.debug('Возникла ошибка в DialogFlow tg-боте')
        logger.exception(e)
