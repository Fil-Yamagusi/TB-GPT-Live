import os
from dotenv import load_dotenv

load_dotenv()

tg = {}
tg['token'] = os.getenv('TG_TOKEN')
tg['eng_name'] = 'FC Fil LiveCoding YaGPT'
tg['name'] = 'fc_fil_lc_yagpt_bot'
tg['addr'] = 'https://t.me/fc_fil_lc_yagpt_bot'
tg['description'] = ('Повторение задания третьего модуля. '
                     'Подсчёт токенов, генерация сценариев')

YaGPT = {}
YaGPT['GPT_MODEL'] = 'yandexgpt-lite'
YaGPT['FOLDER_ID'] = os.getenv('FOLDER_ID')
YaGPT['IAM_TOKEN'] = os.getenv('IAM_TOKEN')

# Для ограничений токенов
MAX_PROJECT_TOKENS = 10000  # макс. количество токенов на весь проект
MAX_USERS = 5  # макс. количество пользователей на весь проект
MAX_SESSIONS = 5  # макс. количество сессий у пользователя
MAX_TOKENS_IN_SESSION = 777  # макс. количество токенов за сессию пользователя

# Для функции count_tokens
MAX_MODEL_TOKENS = 25  # запрос к токенизатору, мы же не просим генерировать?

# Для функции ask_gpt
MAX_ANSWER_TOKENS = 25  # Ограничить длину ответа GPT для экономии
