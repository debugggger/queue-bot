import time

import pytest

from pyrogram import Client

from dotenv import load_dotenv
import os

delay = 0.5

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
def chat_id():
    return int(os.getenv('chat_id'))


@pytest.mark.system
def test_start(client, chat_id):
    client.send_message(chat_id, '/start')
    expected = ("Привет! Я бот для составления очередей.\n"
                "Ты можешь воспользоваться следующими командами, "
                "чтобы более подробно узнать что я умею:")
    time.sleep(delay)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == expected


@pytest.mark.system
def test_show_empty(client, chat_id):
    client.send_message(chat_id, '/show')
    expected = ("Еще нет никаких очередей. Радуйся!")
    time.sleep(delay)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == expected

@pytest.mark.system
def test_show(client, chat_id):
    client.send_message(chat_id, '/subject')
    time.sleep(delay)
    client.send_message(chat_id, 'subject for show')
    time.sleep(delay)
    client.send_message(chat_id, '/create')
    expected = ("По какому предмету ты хочешь создать очередь?")
    time.sleep(delay)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == expected
    client.send_message(chat_id, 'subject for show')
    expected = ("Создана очередь по subject for show")
    time.sleep(delay)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == expected
    client.send_message(chat_id, '/show')
    time.sleep(delay)
    client.send_message(chat_id, 'subject for show')
    expected = ("Очередь по subject for show:")
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == expected

    client.send_message(chat_id, '/delete')
    time.sleep(delay)
    client.send_message(chat_id, 'Очередь по subject for show')
    time.sleep(delay)
    client.send_message(chat_id, '/removesubject')
    time.sleep(delay)
    client.send_message(chat_id, 'subject for show')
    time.sleep(delay)


@pytest.mark.system
def test_confirm_empty(client, chat_id):
    client.send_message(chat_id, '/confirm')
    expected = ("Извините, у вас еще нет запросов на смену места")
    time.sleep(delay)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == expected


@pytest.mark.system
def test_reject_empty(client, chat_id):
    client.send_message(chat_id, '/reject')
    expected = ("Ты еще не записан ни в одну очередь. Ух, ты!")
    time.sleep(delay)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == expected


@pytest.mark.system
def test_create_cancel(client, chat_id):
    client.send_message(chat_id, '/create')
    expected = ("По какому предмету ты хочешь создать очередь?")
    time.sleep(delay)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == expected
    client.send_message(chat_id, '❌ Отмена')
    expected = ("Команда отменена")
    time.sleep(delay)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == expected


@pytest.mark.system
def test_create_correct(client, chat_id):
    client.send_message(chat_id, '/subject')
    time.sleep(delay)
    client.send_message(chat_id, 'subject for create')
    time.sleep(delay)
    client.send_message(chat_id, '/create')
    expected = ("По какому предмету ты хочешь создать очередь?")
    time.sleep(delay)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == expected
    client.send_message(chat_id, 'subject for create')
    expected = ("Создана очередь по subject for create")
    time.sleep(delay)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == expected
    client.send_message(chat_id, '/delete')
    time.sleep(delay)
    client.send_message(chat_id, 'Очередь по subject for create')
    time.sleep(delay)
    client.send_message(chat_id, '/removesubject')
    time.sleep(delay)
    client.send_message(chat_id, 'subject for create')
    time.sleep(delay)
