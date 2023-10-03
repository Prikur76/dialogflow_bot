import os
import json
import logging
from dotenv import load_dotenv

from google.cloud import api_keys_v2
from google.cloud import dialogflow
from error_handler import LogsHandler
import telegram

load_dotenv()


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Создает новое намерение в DialogFlow"""
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=[message_texts])
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )
    request_body = {"parent": parent, "intent": intent}
    response = intents_client.create_intent(
        request=request_body)


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logger.addHandler(LogsHandler())
    logger.setLevel(logging.INFO)
    logger.info('Запускаю обработку файла с диалоговыми данными')

    project_id = os.getenv('PROJECT_ID')
    try:
        intent_file = 'intent_phrases.json'
        with open(intent_file, 'r', encoding='utf-8') as f:
            phrases = json.load(f)
        for theme in phrases:
            display_name = theme
            training_phrases_parts = phrases[theme]['questions']
            message_texts = phrases[theme]['answer']
            create_intent(project_id, display_name,
                          training_phrases_parts, message_texts)
        logger.info('Фразы загружены.')
    except Exception:
        logger.exception('Возникла проблема с загрузкой фраз.')
