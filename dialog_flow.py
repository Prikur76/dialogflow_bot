from google.cloud import api_keys_v2
from google.cloud import dialogflow


class DialogFlow:

    def __init__(self, project_id):
        self.project_id = project_id

    def create_api_key(self):
        """Создает и возвращает объект response с API ключом"""
        client = api_keys_v2.ApiKeysClient()
        key = api_keys_v2.Key()
        key.display_name = f'My API key'

        request = api_keys_v2.CreateKeyRequest()
        request.parent = f'projects/{self.project_id}/locations/global'
        request.key = key

        response = client.create_key(request=request).result()
        print(f'Successfully created an API key: {response.name}')
        return response

    def detect_intent_text(self, session_id, user_message, language_code='ru-RU'):
        """Возвращает ответ из DialogFlow на текстовое сообщение"""
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(self.project_id, session_id)

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
            'answer': response.query_result.fulfillment_text,
            'is_fallback': response.query_result.intent.is_fallback
        }
        return dialogflow_answer

    def create_intent(self, display_name, training_phrases_parts, message_texts):
        """Создает новое намерение в DialogFlow"""
        intents_client = dialogflow.IntentsClient()
        parent = dialogflow.AgentsClient.agent_path(self.project_id)
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
        response = intents_client.create_intent(request=request_body)

    def list_intents(self):
        """Возвращает список намерений указанного агента DialogFlow"""
        intents_client = dialogflow.IntentsClient()
        parent = dialogflow.AgentsClient.agent_path(self.project_id)
        intents = intents_client.list_intents(request={"parent": parent})
        return intents

    def delete_intent(self, intent_id):
        """Удаляет намерение (intent) из агента DialogFlow"""
        intents_client = dialogflow.IntentsClient()
        intent_path = intents_client.intent_path(self.project_id, intent_id)
        intents_client.delete_intent(request={"name": intent_path})
        print('Намерение id {} удалено.'.format(intent_id))

    def display_info(self):
        """Выводит информацию об агенте DialogFlow"""
        print('Project ID: {}'.format(self.project_id))
