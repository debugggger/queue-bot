import pytest
import time

from pyrogram import Client

from dotenv import load_dotenv
import os


DELAY = 0.2

def checkLastMessage(client, chat_id, text: str):
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == text

def checkResponce(client, chat_id, text: str, responceText: str, delay=DELAY):
    client.send_message(chat_id, text)
    time.sleep(delay)
    checkLastMessage(client, chat_id, responceText)


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
def test_subject_incorrectTitle(client, chat_id):
    checkResponce(client, chat_id, '/subject', 'Введи название нового предмета')
    checkResponce(client, chat_id, 'test-subj', 'Название предмета некорректно.\nИспользуйте не более 30 символов русского и английского алфавита.')

@pytest.mark.system
def test_subject(client, chat_id):
    checkResponce(client, chat_id, '/subject', 'Введи название нового предмета')
    checkResponce(client, chat_id, 'subjj', 'Предмет subjj добавлен')
    checkResponce(client, chat_id, '/subject', 'Введи название нового предмета')
    checkResponce(client, chat_id, 'subjj', 'Предмет subjj уже существует')

    client.send_message(chat_id, '/removesubject')
    time.sleep(DELAY)
    client.send_message(chat_id, 'subjj')

@pytest.mark.system
def test_removesubject(client, chat_id):
    client.send_message(chat_id, '/subject')
    time.sleep(DELAY)
    client.send_message(chat_id, 'subjj')

    checkResponce(client, chat_id, '/removesubject', 'Удалить предмет')
    checkResponce(client, chat_id, 'subjj', 'Предмет удален')

@pytest.mark.system
def test_removesubject_cancel(client, chat_id):
    checkResponce(client, chat_id, '/removesubject', 'Удалить предмет')
    checkResponce(client, chat_id, '❌ Отмена', 'Команда отменена')
