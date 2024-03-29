import pytest

import time
import os

import telebot
from pyrogram import Client
from dotenv import load_dotenv
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
