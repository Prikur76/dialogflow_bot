import argparse
import json
import logging
import os

from dotenv import load_dotenv
from google.api_core import exceptions

from dialog_flow import DialogFlow

logger = logging.getLogger(__name__)


def main():
    load_dotenv()
    logging.basicConfig(
        format='[%(levelname)s] - %(asctime)s - %(name)s - %(message)s',
        level=logging.INFO
    )

    parser = argparse.ArgumentParser(
        description='Создает новое намерение в DialogFlow')
    parser.add_argument(
        '--filepath', '-f', type=str, help='Путь до файла с фразами')
    args = parser.parse_args()
    filepath = args.filepath
    if not filepath:
        logger.error('Не указан путь до файла с фразами.')
        return

    try:
        flow = DialogFlow(os.environ.get('PROJECT_ID'))

        with open(filepath, 'r', encoding='utf-8') as f:
            phrases = json.load(f)
        for theme in phrases:
            display_name = theme
            training_phrases_parts = phrases[theme]['questions']
            message_texts = phrases[theme]['answer']
            flow.create_intent(display_name, training_phrases_parts, message_texts)
        logger.info('Фразы загружены.')
    except FileNotFoundError:
        logger.error('Файл с фразами не найден.')
    except exceptions.InvalidArgument as ia_err:
        logger.error('Неверный формат файла с фразами.')
        logger.exception(ia_err, exc_info=False)


if __name__ == '__main__':
    main()
