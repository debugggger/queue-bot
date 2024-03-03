import time
import pytest

from pyrogram import Client

from dotenv import load_dotenv
import os


DELAY = 0.3

def checkLastMessage(client, chat_id, text: str):
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == text

def checkResponce(client, chat_id, text: str, responceText: str, DELAY=DELAY):
    client.send_message(chat_id, text)
    time.sleep(DELAY)
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
def test_removesubject_cancel(client, chat_id):
    checkResponce(client, chat_id, '/removesubject', 'Удалить предмет')
    checkResponce(client, chat_id, '❌ Отмена', 'Команда отменена')


@pytest.mark.system
def test_valid_member(client, chat_id):
    client.send_message(chat_id, '/member')
    time.sleep(DELAY)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == 'Для продолжения нажми кнопку ввод'
    client.send_message(chat_id, 'Ввод')
    time.sleep(DELAY)
    client.send_message(chat_id, 'test-name')
    time.sleep(DELAY)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == 'Отображаемое имя установлено'


@pytest.mark.system
def test_invalid_name(client, chat_id):
    client.send_message(chat_id, '/member')
    time.sleep(DELAY)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == 'Для продолжения нажми кнопку ввод'
    client.send_message(chat_id, 'Ввод')
    time.sleep(DELAY)
    client.send_message(chat_id, 'invalid*((&')
    time.sleep(DELAY)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == ('Отображаемое имя некорректно.\n'
                                      'Используйте не более 30 символов русского и английского алфавита.'
                                      'Также дефис, апостроф, пробел (но не более одного такого символа подряд).')


@pytest.mark.system
def test_delete(client, chat_id):
    client.send_message(chat_id, '/subject')
    time.sleep(DELAY)
    client.send_message(chat_id, 'subjj')
    time.sleep(DELAY)
    client.send_message(chat_id, '/create')
    time.sleep(DELAY)
    client.send_message(chat_id, 'subjj')
    time.sleep(DELAY)
    client.send_message(chat_id, '/delete')
    time.sleep(DELAY)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == 'По какому предмету ты хочешь удалить очередь?'
    time.sleep(DELAY)
    client.send_message(chat_id, 'Очередь по subjj')
    time.sleep(DELAY)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == 'Очередь удалена'

    client.send_message(chat_id, '/removesubject')
    time.sleep(DELAY)
    client.send_message(chat_id, 'Очередь по subjj')


@pytest.mark.system
def test_start(client, chat_id):
    client.send_message(chat_id, '/start')
    expected = ("Привет! Я бот для составления очередей.\n"
                "Ты можешь воспользоваться следующими командами, "
                "чтобы более подробно узнать что я умею:")
    time.sleep(DELAY)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == expected


@pytest.mark.system
def test_show_empty(client, chat_id):
    client.send_message(chat_id, '/show')
    expected = ("Еще нет никаких очередей. Радуйся!")
    time.sleep(DELAY)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == expected


@pytest.mark.system
def test_delete_cancel(client, chat_id):
    client.send_message(chat_id, '/subject')
    time.sleep(DELAY)
    client.send_message(chat_id, 'subjj')
    time.sleep(DELAY)
    client.send_message(chat_id, '/create')
    time.sleep(DELAY)
    client.send_message(chat_id, 'subjj')
    time.sleep(DELAY)
    client.send_message(chat_id, '/delete')
    time.sleep(DELAY)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == 'По какому предмету ты хочешь удалить очередь?'
    time.sleep(DELAY)
    client.send_message(chat_id, '❌ Отмена')
    time.sleep(DELAY)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == 'Команда отменена'

    client.send_message(chat_id, '/removesubject')
    time.sleep(DELAY)
    client.send_message(chat_id, '/incorrect_subj_test')
    time.sleep(DELAY)
    client.send_message(chat_id, '/delete')
    time.sleep(DELAY)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == 'По какому предмету ты хочешь удалить очередь?'
    time.sleep(DELAY)
    client.send_message(chat_id, 'incorrect_subj_test')
    time.sleep(DELAY)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == 'Команда отменена'

    client.send_message(chat_id, '/removesubject')
    time.sleep(DELAY)
    client.send_message(chat_id, 'Очередь по subjj')
    time.sleep(DELAY)
    client.send_message(chat_id, '/removesubject')
    time.sleep(DELAY)
    client.send_message(chat_id, 'Очередь по incorrect_subj_test')


@pytest.mark.system
def test_help(client, chat_id):
    client.send_message(chat_id, '/help')
    time.sleep(DELAY)
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


@pytest.mark.system
def test_removesubject(client, chat_id):
    client.send_message(chat_id, '/subject')
    time.sleep(DELAY)
    client.send_message(chat_id, 'subjj')

    checkResponce(client, chat_id, '/removesubject', 'Удалить предмет')
    checkResponce(client, chat_id, 'subjj', 'Предмет удален')


@pytest.mark.system
def test_show(client, chat_id):
    client.send_message(chat_id, '/subject')
    time.sleep(DELAY)
    client.send_message(chat_id, 'subject for show')
    time.sleep(DELAY)
    client.send_message(chat_id, '/create')
    expected = ("По какому предмету ты хочешь создать очередь?")
    time.sleep(DELAY)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == expected
    client.send_message(chat_id, 'subject for show')
    expected = ("Создана очередь по subject for show")
    time.sleep(DELAY)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == expected
    client.send_message(chat_id, '/show')
    time.sleep(DELAY)
    client.send_message(chat_id, 'subject for show')
    time.sleep(DELAY)
    expected = ("Очередь по subject for show:")
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == expected

    client.send_message(chat_id, '/delete')
    time.sleep(DELAY)
    client.send_message(chat_id, 'Очередь по subject for show')
    time.sleep(DELAY)
    client.send_message(chat_id, '/removesubject')
    time.sleep(DELAY)
    client.send_message(chat_id, 'subject for show')
    time.sleep(DELAY)


@pytest.mark.system
def test_confirm_empty(client, chat_id):
    client.send_message(chat_id, '/confirm')
    expected = ("Извините, у вас еще нет запросов на смену места")
    time.sleep(DELAY)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == expected


@pytest.mark.system
def test_reject_empty(client, chat_id):
    client.send_message(chat_id, '/reject')
    expected = ("Ты еще не записан ни в одну очередь. Ух, ты!")
    time.sleep(DELAY)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == expected


@pytest.mark.system
def test_create_cancel(client, chat_id):
    client.send_message(chat_id, '/create')
    expected = ("По какому предмету ты хочешь создать очередь?")
    time.sleep(DELAY)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == expected
    client.send_message(chat_id, '❌ Отмена')
    expected = ("Команда отменена")
    time.sleep(DELAY)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == expected


@pytest.mark.system
def test_create_correct(client, chat_id):
    client.send_message(chat_id, '/subject')
    time.sleep(DELAY)
    client.send_message(chat_id, 'subject for create')
    time.sleep(DELAY)
    client.send_message(chat_id, '/create')
    expected = ("По какому предмету ты хочешь создать очередь?")
    time.sleep(DELAY)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == expected
    client.send_message(chat_id, 'subject for create')
    expected = ("Создана очередь по subject for create")
    time.sleep(DELAY)
    for message in client.get_chat_history(chat_id, limit=1):
        assert message.text == expected
    client.send_message(chat_id, '/delete')
    time.sleep(DELAY)
    client.send_message(chat_id, 'Очередь по subject for create')
    time.sleep(DELAY)
    client.send_message(chat_id, '/removesubject')
    time.sleep(DELAY)
    client.send_message(chat_id, 'subject for create')
    time.sleep(DELAY)
