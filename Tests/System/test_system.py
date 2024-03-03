import time

import pytest

from pyrogram import Client

from dotenv import load_dotenv
import os

delay = 0.1

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
def test_valid_member(client, chat_id):
    client.send_message(chat_id, '/member')
    time.sleep(delay)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == 'Для продолжения нажми кнопку ввод'
    client.send_message(chat_id, 'Ввод')
    time.sleep(delay)
    client.send_message(chat_id, 'test-name')
    time.sleep(delay)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == 'Отображаемое имя установлено'

@pytest.mark.system
def test_invalid_name(client, chat_id):
    client.send_message(chat_id, '/member')
    time.sleep(delay)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == 'Для продолжения нажми кнопку ввод'
    client.send_message(chat_id, 'Ввод')
    time.sleep(delay)
    client.send_message(chat_id, 'invalid*((&')
    time.sleep(delay)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == ('Отображаемое имя некорректно.\n'
                                      'Используйте не более 30 символов русского и английского алфавита.'
                                      'Также дефис, апостроф, пробел (но не более одного такого символа подряд).')

@pytest.mark.system
def test_delete(client, chat_id):
    client.send_message(chat_id, '/subject')
    time.sleep(delay)
    client.send_message(chat_id, 'subjj')
    time.sleep(delay)
    client.send_message(chat_id, '/create')
    time.sleep(delay)
    client.send_message(chat_id, 'subjj')
    time.sleep(delay)
    client.send_message(chat_id, '/delete')
    time.sleep(delay)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == 'По какому предмету ты хочешь удалить очередь?'
    time.sleep(delay)
    client.send_message(chat_id, 'Очередь по subjj')
    time.sleep(delay)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == 'Очередь удалена'

    client.send_message(chat_id, '/reemovesubject')
    time.sleep(delay)
    client.send_message(chat_id, 'Очередь по subjj')

@pytest.mark.system
def test_delete_cancel(client, chat_id):
    client.send_message(chat_id, '/subject')
    time.sleep(delay)
    client.send_message(chat_id, 'subjj')
    time.sleep(delay)
    client.send_message(chat_id, '/create')
    time.sleep(delay)
    client.send_message(chat_id, 'subjj')
    time.sleep(delay)
    client.send_message(chat_id, '/delete')
    time.sleep(delay)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == 'По какому предмету ты хочешь удалить очередь?'
    time.sleep(delay)
    client.send_message(chat_id, '❌ Отмена')
    time.sleep(delay)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == 'Команда отменена'

    client.send_message(chat_id, '/removesubject')
    time.sleep(delay)
    client.send_message(chat_id, '/incorrect_subj_test')
    time.sleep(delay)
    client.send_message(chat_id, '/delete')
    time.sleep(delay)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == 'По какому предмету ты хочешь удалить очередь?'
    time.sleep(delay)
    client.send_message(chat_id, 'incorrect_subj_test')
    time.sleep(delay)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == 'Команда отменена'

    client.send_message(chat_id, '/reemovesubject')
    time.sleep(delay)
    client.send_message(chat_id, 'Очередь по subjj')
    time.sleep(delay)
    client.send_message(chat_id, '/reemovesubject')
    time.sleep(delay)
    client.send_message(chat_id, 'Очередь по incorrect_subj_test')

@pytest.mark.system
def test_help(client, chat_id):
    client.send_message(chat_id, '/help')
    time.sleep(delay)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == ("можно воспользоваться следующими командами:\n"
                     "/member - добавление в список пользователей\n"
                     "/subject - добавление предмета\n"
                     "/create - создание очереди\n"
                     "/delete - удаление очереди\n"
                     "/show - вывод очереди\n"
                     "/join - запись в последнюю очередь\n"
                     "/jointo - запись в любую из очередей\n"
                     "/replaceto - смена мест c выбором очереди\n"
                     "/replace - смена места в последней очереди\n"
                     "/removefrom - выход из очереди\n"
                     "/removesubject - выход из очереди\n"
                     "/reject - отклонение запроса смены мест\n"
                     "/confirm - подтверждение запроса смены мест")