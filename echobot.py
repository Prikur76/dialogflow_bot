import logging
import os

from dotenv import load_dotenv
from google.cloud import api_keys_v2
from google.cloud import dialogflow
from google.cloud.api_keys_v2 import Key
from telegram import Update, ForceReply
from telegram.ext import (Updater, CommandHandler,
                          MessageHandler, Filters,
                          CallbackContext)

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

project_id = os.getenv('PROJECT_ID')


def create_api_key(project_id: str) -> Key:
    """Создает и возвращает объект response с API ключом"""
    client = api_keys_v2.ApiKeysClient()
    key = api_keys_v2.Key()
    key.display_name = f'My first API key'

    request = api_keys_v2.CreateKeyRequest()
    request.parent = f'projects/{project_id}/locations/global'
    request.key = key

    response = client.create_key(request=request).result()
    print(f'Successfully created an API key: {response.name}')
    return response


def detect_intent_text(project_id, session_id, user_message, language_code='ru-RU'):
    """Возвращает ответ из DialogFlow на текстовое сообщение"""
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(
        text=user_message, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    request_body = {
            'session': session,
            'query_input': query_input
        }
    response = session_client.detect_intent(request=request_body)
    dialogflow_answer = {
        'intent': response.query_result.intent.display_name,
        'confidence': response.query_result.intent_detection_confidence,
        'answer': response.query_result.fulfillment_text
    }
    return dialogflow_answer


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Здравствуй, {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


# def echo(update: Update, context: CallbackContext) -> None:
#     """Echo the user message."""
#     update.message.reply_text(update.message.text)


def echo_dialogflow(update: Update, context: CallbackContext) -> None:
    """Возвращает ответ DialogFlow."""
    user_message = update.message.text
    session_id = update.effective_chat.id
    dialogflow_answer = detect_intent_text(
        project_id, session_id, user_message)
    update.message.reply_text(dialogflow_answer['answer'])


def main() -> None:
    """Start the bot."""
    tg_token = os.getenv("DF_BOT_TOKEN")
    # project_id = os.getenv('PROJECT_ID')
    df_token = create_api_key(project_id)

    updater = Updater(tg_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo_dialogflow)
    )

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
