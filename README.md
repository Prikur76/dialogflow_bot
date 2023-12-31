# "Умные" чат-боты для поддержки в Telegram и ВКонтакте с распознаванием речи.
С помощью **`DialogFlow`** отвечают пользователям на сообщения по заранее загруженному набору фраз. 
Боты легко обучаемы благодаря реализованному функционалу. Если какой-либо бот "сломается", другой, мониторинговый, 
бот сообщит о проблеме.

Если бот во ВКонтакте не отвечает, возможно, был задан вопрос, требующий внимание сотрудника.

Пример tg-бота  ![tg_bot_example](tg_bot_example.gif)     Пример ВК-бота  ![vk_bot_example](vk_bot_example.gif) 


## Как установить

* Python3 должен уже быть установлен.
* Для изоляции проекта рекомендуется использовать [virtualenv/venv](https://docs.python.org/3/library/venv.html).
* Чтобы развернуть зависимости, используйте **`pip`** (или **`pip3`**, если есть конфликт с Python2):

```bash
pip install -r requirements.txt
```
* Для хранения чувствительных данных (токен devman, токен основного бота, токен вспомогательного бота, chat_id пользователя) создайте файл .env 
с переменными **```DF_BOT_TOKEN, SERVICE_BOT_TOKEN, SERVICE_CHAT_ID, VK_COMMUNITY_TOKEN, PROJECT_ID, GOOGLE_APPLICATION_CREDENTIALS```**.

### Этап 1. Получить все авторизационные ключи
#### Этап 1.1 Для запуска бота в Телеграме необходимо:
1) Создать бота для пользователй в telegram через [Отца ботов](https://telegram.me/BotFather) и взять токен для авторизации.
2) Создать бота для сервисных сообщений в telegram через [Отца ботов](https://telegram.me/BotFather) и взять токен для авторизации.
3) Узнать свой ID через [специального бота](https://telegram.me/userinfobot).

#### Этап 1.2 Для запуска бота во Вконтакте необходимо:
1) [Создать сообщество](https://vk.com/groups?tab=admin) или выбрать из уже созданных, где являетесь администратором.
2) Создать сервисный ключ в разделе "Управление" на вкладке "Работа с API"
3) Разрешить отправку сообщений на вкладке "Сообщения".

#### Этап 1.3 Зарегистрироваться и получить ключ авторизации для Dialogflow:
1) Зарегистрироваться на [сайте](https://dialogflow.com/) сервиса.
2) Создать нового агента DialogFlow, получить идентификатор проекта, например, `dialogflow-1234567890`.
3) По инструкции [с сайта Dialogflow](https://cloud.google.com/dialogflow/es/docs/quick/setup) установить консоль gcloud, получить сервисный ключ авторизации и установить необходимые роли.
4) Настройте роль администратора токенов и создайте учетную запись в [GCloud](https://console.cloud.google.com/home/dashboard):
```bash
gcloud projects add-iam-policy-binding <PROJECT_ID>  --member="serviceAccount:<SERVICE_NAME>@<PROJECT_ID>.iam.gserviceaccount.com" --role=roles/serviceusage.apiKeysAdmin
```

### Этап 2. Установить переменные окружения
1) **```DF_BOT_TOKEN```**: токен для основного телеграм-бота (например, **```DF_BOT_TOKEN=95193951:wP3db3301vnrob33BZdb33KwP3db3F1I```**);  
2) **```SERVICE_BOT_TOKEN```**: токен для сервисного телеграм-бота;
3) **```SERVICE_CHAT_ID```**: id пользователя телеграм, который будет получать сервисные сообщения;  
4) **```VK_COMMUNITY_TOKEN```**: токен для бота ВКонтакте, например, **```VK_COMMUNITY_TOKEN=vk1.a.1234567890NKVDJNKSDNVBNKD1234567890-DVJNnvlvDLMERVB1234567890```**;
5) **```PROJECT_ID```**: id проекта в Dialogflow, который можно взять на вкладке 'General' в поле 'Project ID';
6) **```GOOGLE_APPLICATION_CREDENTIALS```**: путь до json-файла с ключом авторизации в Dialogflow.

### Этап 3. Запуск ботов на локальном компьютере

1). Для запуска телеграм-бота в терминале введите следующую команду:

```bash
python tg_bot.py
```

2). Для запуска VK-бота в терминале введите следующую команду:

```bash
python vk_bot.py
```

## Как создать модель "вопрос — ответ" в DialogFlow
#### Cоздание новой темы разговора в DialogFlow:
* На вкладке "Intents" добавить intent (тему) для бота;
* Добавить вопросы и варианты ответов/ответ.

#### Создать список быстрых ответов в DialogFlow:
* На вкладке "Small Talk" добавить ответы на самые популярные вопросы.

#### Создать модель "вопрос — ответ" с помощью файла формата ".json":
* Составить файл со списком тем, вопросов и ответов, например:
```
{
    "Вопросы от действующих партнёров": {
        "questions": [
            "Где проходит совещание",
            "Когда переведёте деньги по контракту",
            "Скоро переведу деньги по контракту",
            "Задерживаемся на совещание",
            "Высылаю итоги совещания",
            "Когда подписываем контракт?",
            "Контракт уже в силе?"
        ],
        "answer": "Простите, в этом чате сидит SMM-отдел, мы не знаем ответа на этот вопрос."
    }
}
```
[Пример файла.](https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json)

* В консоли запустить команду `python` и введите команду 
```bash
python create_intent.py -f <PATH-TO-YOUR-JSON-FILE>
```
где **```<PATH-TO-YOUR-JSON-FILE>```** - путь до json-файла с темами, вопросами и ответами.

Посмотреть справку по аргументам
```bash
python create_intent.py --help
```
### Примеры

* [Пример работающего бота в телеграм](https://t.me/shisterov1_bot);
* [Пример работающего бота в VK](https://vk.com/club219380486).

Intents (намерения) для указанных ботов взяты из [этого файла](https://dvmn.org/media/filer_public/a7/db/a7db66c0-1259-4dac-9726-2d1fa9c44f20/questions.json).

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org).

### Лицензия

Этот проект лицензирован по лицензии MIT - подробности см. в файле [ЛИЦЕНЗИЯ](LICENSE).
