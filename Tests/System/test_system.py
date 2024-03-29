import pytest

import time
import os

import telebot
from pyrogram import Client
from dotenv import load_dotenv

from Services.MemberService import MemberService
from dbTest import DatabaseTest


load_dotenv()
bot_id = int(os.getenv('bot_id'))
chat_id = int(os.getenv('chat_id'))


DELAY = 0.5


def waitBotMessage(client):
    while next(client.get_chat_history(chat_id, limit=1)).from_user.id != bot_id:
        time.sleep(0.3)


def sendAndWaitAny(client, text: str):
    client.send_message(chat_id, text)
    waitBotMessage(client)


def checkResponce(client, text: str, responceText: str, timeout = 30):
    lastMessage = client.send_message(chat_id, text)
    startTime = time.time()
    while True:
        message : telebot.types.Message = next(client.get_chat_history(chat_id, limit=1))
        if (message.from_user.id == bot_id) and (message != lastMessage):
            break
        if time.time() - startTime > timeout:
            assert False
            break
        time.sleep(0.3)
    assert message.text == responceText
    return lastMessage.from_user.id


def create_test_subj(client, chat_id):
    #TODO если в бд есть предмет
    delete_test_subj(client, chat_id)

    client.send_message(chat_id, '/subject')
    time.sleep(DELAY)
    client.send_message(chat_id, 'subject')
    time.sleep(DELAY)


def create_test_queue(client, chat_id):
    create_test_subj(client, chat_id)
    client.send_message(chat_id, '/create')
    expected = ("По какому предмету ты хочешь создать очередь?")
    time.sleep(DELAY)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == expected
    client.send_message(chat_id, 'subject')
    time.sleep(DELAY)


def delete_test_subj(client, chat_id):
    client.send_message(chat_id, '/delete')
    time.sleep(DELAY)
    client.send_message(chat_id, 'Очередь по subject')
    time.sleep(DELAY)


@pytest.fixture(scope="session")
def client():
    load_dotenv()
    api_id = os.getenv('api_id')
    api_hash = os.getenv('api_hash')
    session_string = os.getenv('session_string')
    client = Client(name='client1', api_id=api_id, api_hash=api_hash, in_memory=True, session_string=session_string)
    client.start()
    yield client
    client.stop()


@pytest.fixture(scope="session")
def client2():
    load_dotenv()
    api_id2 = os.getenv('api_id2')
    api_hash2 = os.getenv('api_hash2')
    session_string2 = os.getenv('session_string2')
    client2 = Client(name='client2', api_id=api_id2, api_hash=api_hash2, in_memory=True, session_string=session_string2)
    client2.start()
    yield client2
    client2.stop()


@pytest.fixture(scope='function')
def databaseTest():
    return DatabaseTest()


@pytest.mark.system
def test_valid_member(client, databaseTest):
    clientId = checkResponce(client, '/member', 'Для продолжения нажми кнопку ввод')
    sendAndWaitAny(client, 'Ввод')
    checkResponce(client, 'test-name', 'Отображаемое имя установлено')
    assert MemberService.getMemberByTgNum(databaseTest, int(clientId)).name == 'test-name'




#
# @pytest.mark.system
# def test_subject_incorrectTitle(client):
#     checkResponce(client, '/subject', 'Введи название нового предмета')
#     checkResponce(client, 'test-subj', 'Название предмета некорректно.\nИспользуйте не более 30 символов русского и английского алфавита.')
#
# @pytest.mark.system
# def test_subject(client):
#     checkResponce(client, '/subject', 'Введи название нового предмета')
#     checkResponce(client, 'subjj', 'Предмет subjj добавлен')
#     checkResponce(client, '/subject', 'Введи название нового предмета')
#     checkResponce(client, 'subjj', 'Предмет subjj уже существует')
#
#     sendAndWaitAny(client, '/removesubject')
#     sendAndWaitAny(client, 'subjj')
#
# @pytest.mark.system
# def test_invalid_name(client, chat_id):
#     client.send_message(chat_id, '/member')
#     time.sleep(DELAY)
#     for message in client.get_chat_history(chat_id, limit=1):
#         assert message.text == 'Для продолжения нажми кнопку ввод'
#     client.send_message(chat_id, 'Ввод')
#     time.sleep(DELAY)
#     client.send_message(chat_id, 'invalid*((&')
#     time.sleep(DELAY)
#     for message in client.get_chat_history(chat_id, limit=1):
#         assert message.text == ('Отображаемое имя некорректно.\n'
#                                       'Используйте не более 30 символов русского и английского алфавита.'
#                                       'Также дефис, апостроф, пробел (но не более одного такого символа подряд).')
#
#
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
#
#
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
#
#
#
# @pytest.mark.system
# def test_removesubject(client, chat_id):
#     client.send_message(chat_id, '/subject')
#     time.sleep(DELAY)
#     client.send_message(chat_id, 'subjj')
#
#     checkResponce(client, chat_id, '/removesubject', 'Удалить предмет')
#     checkResponce(client, chat_id, 'subjj', 'Предмет удален')
#
#
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
#
#
# @pytest.mark.system
# def test_confirm_empty(client, chat_id):
#     client.send_message(chat_id, '/confirm')
#     expected = ("Извините, у вас еще нет запросов на смену места")
#     time.sleep(DELAY)
#     for message in client.get_chat_history(chat_id, limit=1):
#         assert message.text == expected
#
#
# @pytest.mark.system
# def test_reject_empty(client, chat_id):
#     client.send_message(chat_id, '/reject')
#     expected = ("Ты еще не записан ни в одну очередь. Ух, ты!")
#     time.sleep(DELAY)
#     for message in client.get_chat_history(chat_id, limit=1):
#         assert message.text == expected
#
#
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
#
#
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
#
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
#
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
#
#
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
#
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
