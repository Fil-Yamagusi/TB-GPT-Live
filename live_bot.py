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

import config

TG_TOKEN = config.tg['token']
