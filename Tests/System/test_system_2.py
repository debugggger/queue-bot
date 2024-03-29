import pytest

import time
import os

import telebot
from telebot import types
from pyrogram import Client
from dotenv import load_dotenv

from Services.MemberService import MemberService
from Services.SubjectService import SubjectService
from Services.QueueService import QueueService

from test_common import *
from utils import formReplaceRequest


# 12
@pytest.mark.system
def test_create_cancel(client):
    checkResponce(client, '/create', 'По какому предмету ты хочешь создать очередь?')
    checkResponce(client, '❌ Отмена', 'Команда отменена')

# 13
@pytest.mark.system
def test_create_correct(client):
    sendAndWaitAny(client, '/subject')
    sendAndWaitAny(client, 'subject for create')

    checkResponce(client, '/create', 'По какому предмету ты хочешь создать очередь?')
    checkResponce(client, 'subject for create', 'Создана очередь по subject for create')

    sendAndWaitAny(client, '/delete')
    sendAndWaitAny(client, 'Очередь по subject for create')
    sendAndWaitAny(client, '/removesubject')
    sendAndWaitAny(client, 'subject for create')

# 14
@pytest.mark.system
def test_join_last(client, client2, databaseTest):
    create_test_queue(client, chat_id)

    checkResponce(client, '/join', 'Выбрана очередь по subject:\nВыбери место для записи')
    expected = f'Ты записан на {MemberService.getMembersCount(databaseTest)} место'
    checkResponce(client, 'Последнее свободное', expected)

    checkResponce(client2, '/join', 'Выбрана очередь по subject:\nВыбери место для записи')
    expected = f'Ты записан на {MemberService.getMembersCount(databaseTest) - 1} место'
    checkResponce(client2, 'Последнее свободное', expected)

    delete_test_subj(client, chat_id)

# 15
@pytest.mark.system
def test_join_first(client, client2, databaseTest):
    create_test_queue(client, chat_id)

    checkResponce(client, '/join', 'Выбрана очередь по subject:\nВыбери место для записи')
    checkResponce(client, 'Первое свободное', 'Ты записан на 1 место')

    checkResponce(client2, '/join', 'Выбрана очередь по subject:\nВыбери место для записи')
    checkResponce(client2, 'Первое свободное', 'Ты записан на 2 место')

    delete_test_subj(client, chat_id)

# 16
@pytest.mark.system
def test_join_num(client, client2):
    create_test_queue(client, chat_id)

    checkResponce(client, '/join', 'Выбрана очередь по subject:\nВыбери место для записи')
    checkResponce(client, 'Определенное', 'Введи место для записи')
    checkResponce(client, '2', 'Ты записан на 2 место')

    checkResponce(client2, '/join', 'Выбрана очередь по subject:\nВыбери место для записи')
    checkResponce(client2, 'Определенное', 'Введи место для записи')
    checkResponce(client2, '2', 'Желаемое место уже занято или превышает количество человек, которые живут очередями. Ты записан на 3 место')

    delete_test_subj(client, chat_id)


# 17 (возможно не работает)
@pytest.mark.systemCurr
def test_confirm(client, client2):
    create_test_queue(client, chat_id)

    sendAndWaitAny(client, '/join')
    sendAndWaitAny(client, 'Определенное')
    msg1: types.Message = sendAndWaitAny(client, '1')

    sendAndWaitAny(client2, '/join')
    sendAndWaitAny(client2, 'Определенное')
    msg2: types.Message = sendAndWaitAny(client2, '2')

    replaceRequestText = formReplaceRequest(msg1.from_user.username, msg2.from_user.username, 'subject', 1, 2)
    checkResponce(client2, '/replace', 'Выбрана очередь по subject:\nВведи место с которым хочешь поменяться')
    checkResponce(client2, '1', replaceRequestText)

    checkResponce(client, '/confirm', 'Смена мест произошла успешно!')

    delete_test_subj(client, chat_id)
