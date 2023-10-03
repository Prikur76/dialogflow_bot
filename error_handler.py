import logging
import os

from dotenv import load_dotenv
import telegram

load_dotenv()

class LogsHandler(logging.Handler):
    def emit(self, record):
        tg_token = os.getenv('DF_BOT_TOKEN')
        chat_id = os.getenv('CHAT_ID')
        log_entry = self.format(record)
        bot_error = telegram.Bot(token=tg_token)
        bot_error.send_message(chat_id=chat_id, text=log_entry)
