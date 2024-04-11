import os
from dotenv import load_dotenv

load_dotenv()

# Настройки для телеграм-бота (не авторизация!)
tg = {}
tg['token'] = os.getenv('TG_TOKEN')
tg['eng_name'] = 'FC Fil LiveCoding YaGPT'
tg['name'] = 'fc_fil_lc_yagpt_bot'
tg['addr'] = 'https://t.me/fc_fil_lc_yagpt_bot'
tg['description'] = ('Повторение задания третьего модуля. '
                     'Подсчёт токенов, генерация сценариев')

# Настройки для БД (не авторизация!)
DB = {}
DB['db_file'] = "live_db.db"

# Настройки для общения с YaGPT (не авторизация!)
YaGPT = {}
YaGPT['GPT_MODEL'] = 'yandexgpt-lite'
YaGPT['FOLDER_ID'] = os.getenv('FOLDER_ID')
YaGPT['IAM_TOKEN'] = os.getenv('IAM_TOKEN')

# Для ограничений токенов
YaGPT['MAX_PROJECT_TOKENS'] = 10000  # макс. количество токенов на весь проект
YaGPT['MAX_USERS'] = 5  # макс. количество пользователей на весь проект
YaGPT['MAX_SESSIONS'] = 5  # макс. количество сессий у пользователя
YaGPT['MAX_TOKENS_IN_SESSION'] = 777  # макс. количество токенов за сессию пользователя

# Для функции count_tokens
YaGPT['MAX_MODEL_TOKENS'] = 25  # запрос к токенизатору, мы же не просим генерировать?

# Для функции ask_gpt
YaGPT['MAX_ANSWER_TOKENS'] = 25  # Ограничить длину ответа GPT для экономии
