import pytest

import time
import os

import telebot
from pyrogram import Client
from dotenv import load_dotenv

from Services.MemberService import MemberService
from Services.SubjectService import SubjectService
from Services.QueueService import QueueService

from test_common import *


# 12
# @pytest.mark.system
# def test_create_cancel(client, chat_id):
#     client.send_message(chat_id, '/create')
#     expected = ("По какому предмету ты хочешь создать очередь?")
#     time.sleep(DELAY)
#     for message in client.get_chat_history(chat_id, limit=1):
#         assert message.text == expected
#     client.send_message(chat_id, '❌ Отмена')
#     expected = ("Команда отменена")
#     time.sleep(DELAY)
#     for message in client.get_chat_history(chat_id, limit=1):
#         assert message.text == expected


# 13
# @pytest.mark.system
# def test_create_correct(client, chat_id):
#     client.send_message(chat_id, '/subject')
#     time.sleep(DELAY)
#     client.send_message(chat_id, 'subject for create')
#     time.sleep(DELAY)
#     client.send_message(chat_id, '/create')
#     expected = ("По какому предмету ты хочешь создать очередь?")
#     time.sleep(DELAY)
#     for message in client.get_chat_history(chat_id, limit=1):
#         assert message.text == expected
#     client.send_message(chat_id, 'subject for create')
#     expected = ("Создана очередь по subject for create")
#     time.sleep(DELAY)
#     for message in client.get_chat_history(chat_id, limit=1):
#         assert message.text == expected
#     client.send_message(chat_id, '/delete')
#     time.sleep(DELAY)
#     client.send_message(chat_id, 'Очередь по subject for create')
#     time.sleep(DELAY)
#     client.send_message(chat_id, '/removesubject')
#     time.sleep(DELAY)
#     client.send_message(chat_id, 'subject for create')
#     time.sleep(DELAY)


# 14
# @pytest.mark.system
# def test_join_last(client, client2, chat_id):
#     create_test_queue(client, chat_id)
#
#     client.send_message(chat_id, '/join')
#     time.sleep(DELAY)
#     client.send_message(chat_id, 'Последнее свободное')
#     time.sleep(DELAY)
#     #TODO проверить что чел записан на мсесто, равное количесвту записей в мемберах
#
#     client2.send_message(chat_id, '/join')
#     time.sleep(DELAY)
#     client2.send_message(chat_id, 'Последнее свободное')
#     time.sleep(DELAY)
#     #TODO проверить что чел записан на мсесто, равное количесвту записей в мемберах -1
#
#     delete_test_subj(client, chat_id)


# 15
# @pytest.mark.system
# def test_join_first(client, databaseTest):
#     create_test_queue(client, chat_id)
#
#     client.send_message(chat_id, '/join')
#     time.sleep(DELAY)
#     client1Id = client.send_message(chat_id, 'Первое свободное').from_user.id
#     time.sleep(DELAY)
#
#
#     #TODO проверить что чел записан на первое место
#     with databaseTest.connection.cursor() as cur:
#         cur.execute("select * from subjects where id_subject=%s", (client1Id,))
#         #result = cur.fetchall()[0]
#
#
#     client2.send_message(chat_id, '/join')
#     time.sleep(DELAY)
#     client2.send_message(chat_id, 'Первое свободное')
#     time.sleep(DELAY)
#     #TODO проверить что чел записан на второе место
#
#     delete_test_subj(client, chat_id)


# 16
# @pytest.mark.system
# def test_join_num(client, chat_id):
#     create_test_queue(client, chat_id)
#
#     client.send_message(chat_id, '/join')
#     time.sleep(DELAY)
#     client.send_message(chat_id, 'Определенное')
#     time.sleep(DELAY)
#     client.send_message(chat_id, '2')
#     time.sleep(DELAY)
#     #TODO проверить что чел записан на второе место
#
#     client2.send_message(chat_id, '/join')
#     time.sleep(DELAY)
#     client2.send_message(chat_id, 'Определенное')
#     time.sleep(DELAY)
#     client2.send_message(chat_id, '2')
#     time.sleep(DELAY)
#     #TODO проверить что чел записан на 3 место
#
#     delete_test_subj(client, chat_id)


# 17
# @pytest.mark.system
# def test_confirm(client, chat_id):
#     create_test_queue(client, chat_id)
#
#     client.send_message(chat_id, '/join')
#     time.sleep(DELAY)
#     client.send_message(chat_id, 'Определенное')
#     time.sleep(DELAY)
#     client.send_message(chat_id, '1')
#     time.sleep(DELAY)
#     client2.send_message(chat_id, '/join')
#     time.sleep(DELAY)
#     client2.send_message(chat_id, 'Определенное')
#     time.sleep(DELAY)
#     client2.send_message(chat_id, '2')
#     time.sleep(DELAY)
#
#     client.send_message(chat_id, '/replace')
#     time.sleep(DELAY)
#     client.send_message(chat_id, '2')
#     time.sleep(DELAY)
#     # TODO проверить что произошла смена
#
#     delete_test_subj(client, chat_id)
