import logging
import os
import random

import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

from dialog_flow import DialogFlow
from error_handler import LogsHandler

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def echo(event, vk_api):
    user_id = event.user_id
    user_message = event.text
    try:
        flow = DialogFlow(os.getenv('PROJECT_ID'))
        flow_answer = flow.detect_intent_text(
            user_id, user_message)
        if not flow_answer['is_fallback']:
            vk_api.messages.send(
                user_id=user_id,
                message=flow_answer['answer'],
                random_id=random.randint(1, 1000000000)
            )
    except Exception:
        logging.exception('Проблема с получением/отправкой сообщений')


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(LogsHandler())
    logger.info('VK бот запущен')

    try:
        vk_session = vk.VkApi(token=os.getenv('VK_ACCESS_TOKEN'))
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                echo(event, vk_api)
    except Exception:
        logger.exception('Возникла ошибка в VK боте')
