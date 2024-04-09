# #!/usr/bin/env python3.12
# # -*- coding: utf-8 -*-
#
# # 2024-04-09
# # https://www.twitch.tv/b1nc0d3z
#
# Future code Yandex.Practicum
# AI-bot: Scenario generator
# README.md for more
#
# FC Fil LiveCoding YaGPT
# @fc_fil_lc_yagpt_bot
# https://t.me/fc_fil_lc_yagpt_bot

__version__ = '1.0'
__author__ = 'Firip Yamagusi'

import random
from time import time_ns, time, strftime
from random import choice

import logging

from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, Message

from config import tg

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt="%F %T", )
logging.info("Start")

TG_TOKEN = tg['token']
bot = TeleBot(TG_TOKEN)

HEROES = [
    'Лёлик',
    'Болек',
    'Маша с косичкой',
    'Даша с бидонами',
]

def create_keyboard(buttons: list):
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        row_width=2,
        one_time_keyboard=True
    )
    markup.add(*buttons)
    return markup


@bot.message_handler(commands=['start'])
def handle_start(message: Message):
    # welcome and starting command
    mcid = message.chat.id
    logging.info(f"/start from {mcid = }")
    bot.send_message(
        mcid,
        f"Hi, {message.from_user.first_name}!",
    )


@bot.message_handler(commands=['new_chat'])
def handle_new_chat(message: Message):
    # welcome and starting command
    mcid = message.chat.id
    logging.info(f"/new_chat from {mcid = }")
    bot.send_message(
        mcid,
        f"Для начала выбери жанр.",
        reply_markup=create_keyboard(HEROES)
    )


def process_heroes(m: Message):
    # process hero selection
    mcid = message.chat.id
    if m.text not in HEROES:
        bot.send_message(
            mcid,
            f"Выбери ГЕРОЯ!",
            reply_markup=create_keyboard(HEROES)
        )
        bot.register_next_step_handler(m, process_heroes)
        return

bot.polling(none_stop=True)
logging.info("Finish")
