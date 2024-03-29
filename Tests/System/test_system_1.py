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


# 1
@pytest.mark.system
def test_add_invalid_member(client, databaseTest):
    clientId = checkResponce(client, '/member', 'Для продолжения нажми кнопку ввод')
    sendAndWaitAny(client, 'Ввод')
    checkResponce(client, 'invalid*((&', 'Отображаемое имя некорректно.\n'
                                      'Используйте не более 30 символов русского и английского алфавита.'
                                      'Также дефис, апостроф, пробел (но не более одного такого символа подряд).')
    # Проверяем, что пользователь НЕ был добавлен
    assert not MemberService.isMemberExistByTgNum(databaseTest, int(clientId))


# 2
@pytest.mark.system
def test_add_valid_member(client, databaseTest):
    clientId = checkResponce(client, '/member', 'Для продолжения нажми кнопку ввод')
    sendAndWaitAny(client, 'Ввод')
    checkResponce(client, 'test-name', 'Отображаемое имя установлено')
    assert MemberService.getMemberByTgNum(databaseTest, int(clientId)).name == 'test-name'
    # Проверяем второй раз, что мы меняем имя тому же пользователю
    clientId = checkResponce(client, '/member', 'Для продолжения нажми кнопку ввод')
    sendAndWaitAny(client, 'Ввод')
    checkResponce(client, 'another-name', 'Отображаемое имя установлено')
    assert MemberService.getMemberByTgNum(databaseTest, int(clientId)).name == 'another-name'


# 3 (почему-то не работает)
# @pytest.mark.system
def test_add_invalid_subject(client, databaseTest):
    checkResponce(client, '/subject', 'Введи название нового предмета')
    checkResponce(client, 'thisisverylongtitleforsubjectmore30letters', 'Название предмета некорректно.\nИспользуйте не более 30 символов русского и английского алфавита.')
    # Проверяем, что предмет НЕ был добавлен
    assert not SubjectService.getSubjectByTitle(databaseTest, 'thisisverylongtitleforsubjectmore30letters').title == 'thisisverylongtitleforsubjectmore30letters'


# 4
@pytest.mark.system
def test_add_valid_subject(client, databaseTest):
    checkResponce(client, '/subject', 'Введи название нового предмета')
    checkResponce(client, 'subjj', 'Предмет subjj добавлен')
    # Проверяем, что предмет был добавлен
    assert SubjectService.getSubjectByTitle(databaseTest, 'subjj').title == 'subjj'

    checkResponce(client, '/subject', 'Введи название нового предмета')
    checkResponce(client, 'subjj', 'Предмет subjj уже существует')
    # Проверяем, что таких предметов все равно осталась одна штука
    assert SubjectService.isSubjectExist(databaseTest, 'subjj')

    sendAndWaitAny(client, '/removesubject')
    sendAndWaitAny(client, 'subjj')


# 5
@pytest.mark.system
def test_remove_subject(client, databaseTest):
    checkResponce(client, '/subject', 'Введи название нового предмета')
    checkResponce(client, 'subjj', 'Предмет subjj добавлен')
    checkResponce(client, '/removesubject', 'Удалить предмет')
    checkResponce(client, 'subjj', 'Предмет удален')
    # Проверяем, что предмет был удален
    assert not SubjectService.isSubjectExist(databaseTest, 'subjj')


# 6
@pytest.mark.system
def test_create_queue(client, databaseTest):
    checkResponce(client, '/subject', 'Введи название нового предмета')
    checkResponce(client, 'subjj', 'Предмет subjj добавлен')
    checkResponce(client, '/create', 'По какому предмету ты хочешь создать очередь?')
    checkResponce(client, 'subjj', 'Создана очередь по subjj')
    assert QueueService.isQueueExist(databaseTest,
                                     SubjectService.getSubjectByTitle(databaseTest, 'subjj').id)
    checkResponce(client, '/delete', 'По какому предмету ты хочешь удалить очередь?')
    checkResponce(client, 'Очередь по subjj', 'Очередь удалена')
    checkResponce(client, '/removesubject', 'Удалить предмет')
    checkResponce(client, 'subjj', 'Предмет удален')


# 7
# @pytest.mark.system
# def test_delete(client, chat_id):
#     client.send_message(chat_id, '/subject')
#     time.sleep(DELAY)
#     client.send_message(chat_id, 'subjj')
#     time.sleep(DELAY)
#     client.send_message(chat_id, '/create')
#     time.sleep(DELAY)
#     client.send_message(chat_id, 'subjj')
#     time.sleep(DELAY)
#     client.send_message(chat_id, '/delete')
#     time.sleep(DELAY)
#     for message in client.get_chat_history(chat_id, limit=1):
#         assert message.text == 'По какому предмету ты хочешь удалить очередь?'
#     time.sleep(DELAY)
#     client.send_message(chat_id, 'Очередь по subjj')
#     time.sleep(DELAY)
#     for message in client.get_chat_history(chat_id, limit=1):
#         assert message.text == 'Очередь удалена'
#
#     client.send_message(chat_id, '/removesubject')
#     time.sleep(DELAY)
#     client.send_message(chat_id, 'Очередь по subjj')


# 8
# @pytest.mark.system
# def test_delete_cancel(client, chat_id):
#     client.send_message(chat_id, '/subject')
#     time.sleep(DELAY)
#     client.send_message(chat_id, 'subjj')
#     time.sleep(DELAY)
#     client.send_message(chat_id, '/create')
#     time.sleep(DELAY)
#     client.send_message(chat_id, 'subjj')
#     time.sleep(DELAY)
#     client.send_message(chat_id, '/delete')
#     time.sleep(DELAY)
#     for message in client.get_chat_history(chat_id, limit=1):
#         assert message.text == 'По какому предмету ты хочешь удалить очередь?'
#     time.sleep(DELAY)
#     client.send_message(chat_id, '❌ Отмена')
#     time.sleep(DELAY)
#     for message in client.get_chat_history(chat_id, limit=1):
#         assert message.text == 'Команда отменена'
#
#     client.send_message(chat_id, '/removesubject')
#     time.sleep(DELAY)
#     client.send_message(chat_id, '/incorrect_subj_test')
#     time.sleep(DELAY)
#     client.send_message(chat_id, '/delete')
#     time.sleep(DELAY)
#     for message in client.get_chat_history(chat_id, limit=1):
#         assert message.text == 'По какому предмету ты хочешь удалить очередь?'
#     time.sleep(DELAY)
#     client.send_message(chat_id, 'incorrect_subj_test')
#     time.sleep(DELAY)
#     for message in client.get_chat_history(chat_id, limit=1):
#         assert message.text == 'Команда отменена'
#
#     client.send_message(chat_id, '/removesubject')
#     time.sleep(DELAY)
#     client.send_message(chat_id, 'Очередь по subjj')
#     time.sleep(DELAY)
#     client.send_message(chat_id, '/removesubject')
#     time.sleep(DELAY)
#     client.send_message(chat_id, 'Очередь по incorrect_subj_test')


# 9
# @pytest.mark.system
# def test_show(client, chat_id):
#     client.send_message(chat_id, '/subject')
#     time.sleep(DELAY)
#     client.send_message(chat_id, 'subject for show')
#     time.sleep(DELAY)
#     client.send_message(chat_id, '/create')
#     expected = ("По какому предмету ты хочешь создать очередь?")
#     time.sleep(DELAY)
#     for message in client.get_chat_history(chat_id, limit=1):
#         assert message.text == expected
#     client.send_message(chat_id, 'subject for show')
#     expected = ("Создана очередь по subject for show")
#     time.sleep(DELAY)
#     for message in client.get_chat_history(chat_id, limit=1):
#         assert message.text == expected
#     client.send_message(chat_id, '/show')
#     time.sleep(DELAY)
#     client.send_message(chat_id, 'subject for show')
#     time.sleep(DELAY)
#     expected = ("Очередь по subject for show:")
#     for message in client.get_chat_history(chat_id, limit=1):
#         assert message.text == expected
#
#     client.send_message(chat_id, '/delete')
#     time.sleep(DELAY)
#     client.send_message(chat_id, 'Очередь по subject for show')
#     time.sleep(DELAY)
#     client.send_message(chat_id, '/removesubject')
#     time.sleep(DELAY)
#     client.send_message(chat_id, 'subject for show')
#     time.sleep(DELAY)


# 10
# @pytest.mark.system
# def test_confirm_empty(client, chat_id):
#     client.send_message(chat_id, '/confirm')
#     expected = ("Извините, у вас еще нет запросов на смену места")
#     time.sleep(DELAY)
#     for message in client.get_chat_history(chat_id, limit=1):
#         assert message.text == expected


# 11
# @pytest.mark.system
# def test_reject_empty(client, chat_id):
#     client.send_message(chat_id, '/reject')
#     expected = ("Ты еще не записан ни в одну очередь. Ух, ты!")
#     time.sleep(DELAY)
#     for message in client.get_chat_history(chat_id, limit=1):
#         assert message.text == expected

