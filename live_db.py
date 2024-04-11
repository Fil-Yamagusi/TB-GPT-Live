# #!/usr/bin/env python3.12
# # -*- coding: utf-8 -*-
#
# работа с БД для бота-сценариста

__version__ = '1.0'
__author__ = 'Firip Yamagusi'

import logging
import sqlite3

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt="%F %T", )

logging.warning(f"Start DB file")


def create_db(db_file) -> sqlite3.Cursor:
    # создание БД-файла, если не было. Создание таблиц, если не было

    with sqlite3.connect(db_file, check_same_thread=False) as db_connection:
        cursor = db_connection.cursor()

        # Создаем таблицу Sessions
        # Здесь для статистики хранятся настройки на момент запроса
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS Sessions ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'user_id INTEGER, '
            'genre TEXT, '
            'character TEXT, '
            'entourage TEXT, '
            't_start INT, '
            'task TEXT, '
            'answer TEXT'
            ')'
        )
        logging.info(f"CREATE TABLE IF NOT EXISTS Sessions")

        # Создаем таблицу Prompts
        # Словарь для хранения истории диалога пользователя и GPT
        # Он же хранится в user_data[user_id]['collection']
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS Prompts ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'user_id INTEGER, '
            'session_id INTEGER, '
            'role TEXT, '
            'content TEXT, '
            'tokens INT'
            ')'
        )
        logging.info(f"CREATE TABLE IF NOT EXISTS Prompts")

        # Создаем таблицу Tokenizer
        # Храним обращения к токенайзеру
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS Tokenizer ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'user_id INTEGER, '
            'session_id INTEGER, '
            't_start INTEGER, '
            'content TEXT, '
            'tokens INT'
            ')'
        )
        logging.info(f"CREATE TABLE IF NOT EXISTS Tokenizer")

        # Создаем таблицу Full_Stories
        # Храним итоговые сочинения для смеха
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS Full_Stories ('
            'id INTEGER PRIMARY KEY, '
            'user_id INTEGER, '
            'session_id INTEGER, '
            'content TEXT'
            ')'
        )
        logging.info(f"CREATE TABLE IF NOT EXISTS Full_Stories")

        return True

    return False


logging.warning("Finish DB file")
