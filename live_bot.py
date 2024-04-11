# #!/usr/bin/env python3.12
# # -*- coding: utf-8 -*-
#
# # 2024-04-09 https://www.twitch.tv/b1nc0d3z
#
# Код будущего. Яндекс.Практикум
# ИИ-бот. Генератор сценариев
# README.md для подробностей
#
# https://t.me/fc_fil_lc_yagpt_bot

__version__ = '1.1'
__author__ = 'Firip Yamagusi'

# from time import time_ns, time, strftime
# from random import choice

# Стандартные модули
import logging

import live_db
# специальные модули
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, Message

# собственные модули
from config import tg, DB
from live_db import create_db

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt="%F %T", )
logging.warning("Start")

TG_TOKEN = tg['token']

bot = TeleBot(TG_TOKEN)

# Убирать кнопки для простых сообщений
hideKeyboard = ReplyKeyboardRemove()

# Вспомогательные словари для настроек
STATES = ['hero', 'genre', 'entourage']

HEROES = ['Лёлик', 'Болек',
          'Маша с косичкой', 'Даша с бидонами', ]
GENRES = ['Басня', 'Эпос', 'Анекдот', 'Притча', ]
ENTOURAGES = ['Базарная площадь', 'Тесный лифт',
              'Палуба Титаника', 'Урок ОБЖ', ]

# Большой словарь для выбора настроек
CONTENT = {
    'hero': {
        'text': 'Выбери героя: ',
        'buttons': HEROES,
    },
    'genre': {
        'text': 'Выбери жанр: ',
        'buttons': GENRES,
    },
    'entourage': {
        'text': 'Выбери антураж: ',
        'buttons': ENTOURAGES,
    },
}

# Короткое имя для словаря с настройками и состоянием пользователя
data = {}


def check_user(m: Message):
    # Проверяет, есть ли сейчас данный пользователь в data
    return data.get(m.chat.id)


def create_keyboard(buttons: list) -> ReplyKeyboardMarkup:
    # Создаём клавиатуру для разных этапов настройки
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2,
        one_time_keyboard=True
    ).add(*buttons)


@bot.message_handler(commands=['start'])
def handle_start(m: Message) -> Message:
    # Приветствие. Возможно, тут обнулять состояния буду
    global data
    mcid = m.chat.id
    logging.info(f"/start from {mcid = }")

    bot.send_message(
        mcid,
        f"Hi, {m.from_user.first_name}!",
        reply_markup=hideKeyboard,
    )


@bot.message_handler(commands=['new_scenario'])
def handle_new_scenario(m: Message) -> Message:
    # Создаю новый чат
    global data
    mcid = m.chat.id
    logging.info(f"/new_scenario from {mcid = }")
    data[mcid] = {}
    data[mcid]['state'] = 0
    state = STATES[data[mcid]['state']]

    bot.send_message(
        mcid,
        f"Начинаем создавать новый сценарий!",
        reply_markup=hideKeyboard,
    )
    bot.send_message(
        mcid,
        f"{CONTENT[state]['text']}",
        reply_markup=create_keyboard(CONTENT[state]['buttons'])
    )
    bot.register_next_step_handler(m, process_settings)


def process_settings(m: Message) -> Message:
    # Настройки пошагово заполняю
    global data
    mcid = m.chat.id
    logging.info(f"/process_settings from {mcid = }")
    state = STATES[data[mcid]['state']]

    # Надо выбрать точное значение. Удобнее - с кнопок
    if m.text not in CONTENT[state]['buttons']:
        bot.send_message(
            mcid,
            f"Пожалуйста, выбери кнопками!\n\n"
            f"{CONTENT[state]['text']}",
            reply_markup=create_keyboard(CONTENT[state]['buttons'])
        )
        bot.register_next_step_handler(m, process_settings)
        return
    else:
        data[mcid][state] = m.text
        # Если все настройки введены, то выхожу
        if data[mcid]['state'] == len(STATES) - 1:
            bot.send_message(
                mcid,
                f"Неплохо, все настройки готовы. "
                f"Можешь указать уточняющую информацию для бота:\n"
                f"/additional_info",
                reply_markup=hideKeyboard,
            )
            # bot.register_next_step_handler(m, handle_ask_gpt)
            return

        # Если не все, то продолжаю вводить
        data[mcid]['state'] += 1
        state = STATES[data[mcid]['state']]
        bot.send_message(
            mcid,
            f"{CONTENT[state]['text']}",
            reply_markup=create_keyboard(CONTENT[state]['buttons'])
        )
        bot.register_next_step_handler(m, process_settings)


@bot.message_handler(commands=['additional_info'], func=check_user)
def handle_additional_info(m: Message) -> Message:
    # по ТЗ можно опционально задать GPT доп информацию
    global data
    mcid = m.chat.id
    logging.info(f"handle_additional_info from {mcid = }")

    bot.send_message(
        mcid,
        f"Введи дополнительную уточняющую информацию для сценария:",
        reply_markup=hideKeyboard,
    )
    bot.register_next_step_handler(m, process_additional_info)


def process_additional_info(m: Message) -> Message:
    # Сохраняю доп информации от пользователя
    global data
    mcid = m.chat.id
    logging.info(f"process_additional_info from {mcid = }")

    data[mcid]['additional'] = m.text
    bot.send_message(
        mcid,
        f"Спасибо за уточнение!\n\n"
        f"Теперь можешь вводить запросы к YaGPT.",
        reply_markup=hideKeyboard,
    )


@bot.message_handler(content_types=['text'], func=check_user)
def handle_ask_gpt(m: Message) -> Message:
    # Тут начинаются запросы к GPT
    global data
    mcid = m.chat.id
    logging.info(f"handle_ask_gpt from {mcid = }")

    bot.send_message(
        mcid,
        f"Тут начинается возня с запросами",
        reply_markup=hideKeyboard,
    )


@bot.message_handler(content_types=['text'])
@bot.message_handler(commands=['help'])
def handle_help(m: Message) -> Message:
    # Реакция на /help или нежданное сообщение пользователя
    mcid = m.chat.id
    logging.info(f"handle_ask_gpt from {mcid = }")
    bot.send_message(
        mcid,
        f"Этот бот помогает создавать сценарии с помощью YaGPT.\n\n"
        f"Введи команду /new_scenario для начала работы.",
        reply_markup=hideKeyboard,
    )


# вызываем создание БД
res = create_db(DB['db_file'])
logging.info(f"Create DB and tables {res = }")

# Бот крутится, запросы мутятся
bot.polling(none_stop=True)
logging.warning("Finish")
