# #!/usr/bin/env python3.12
# # -*- coding: utf-8 -*-
#
# # 2024-04-09 https://www.twitch.tv/b1nc0d3z
#
# Future code Yandex.Practicum
# AI-bot: Scenario generator
# README.md for more
#
# https://t.me/fc_fil_lc_yagpt_bot

__version__ = '1.1'
__author__ = 'Firip Yamagusi'

# from time import time_ns, time, strftime
# from random import choice

import logging

from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, Message

from config import tg

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


def create_keyboard(buttons: list) -> ReplyKeyboardMarkup:
    # Создаём клавиатуру для разных этапов настройки
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2,
        one_time_keyboard=True
    ).add(*buttons)


@bot.message_handler(commands=['start'])
def handle_start(m: Message) -> Message:
    # welcome and starting command
    global data
    mcid = m.chat.id
    logging.info(f"/start from {mcid = }")

    bot.send_message(
        mcid,
        f"Hi, {m.from_user.first_name}!",
        reply_markup=hideKeyboard,
    )


@bot.message_handler(commands=['new_chat'])
def handle_new_chat(m: Message) -> Message:
    # Приветсвенная команда, она же - создание нового чата
    global data
    mcid = m.chat.id
    logging.info(f"/new_chat from {mcid = }")
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
    # Настройки постепенно заполняем
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
        # Если все настройки введены, то выходим
        if data[mcid]['state'] == len(STATES) - 1:
            bot.send_message(
                mcid,
                f"Неплохо, все настройки готовы. Пора в GPT!",
                reply_markup=hideKeyboard,
            )
            bot.register_next_step_handler(m, handle_ask_gpt)
            return

        # Если не все, то продолжаем вводить
        data[mcid]['state'] += 1
        state = STATES[data[mcid]['state']]
        bot.send_message(
            mcid,
            f"{CONTENT[state]['text']}",
            reply_markup=create_keyboard(CONTENT[state]['buttons'])
        )
        bot.register_next_step_handler(m, process_settings)


def handle_ask_gpt(m: Message) -> Message:
    # Тут начинаются запросы к GPT
    global data
    mcid = m.chat.id
    logging.info(f"/handle_ask_gpt from {mcid = }")

    bot.send_message(
        mcid,
        f"Тут начинается возня с запросами",
        reply_markup=hideKeyboard,
    )


bot.polling(none_stop=True)
logging.warning("Finish")
